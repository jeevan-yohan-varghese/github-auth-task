import uvicorn

from fastapi import FastAPI, Depends, HTTPException,Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from github import Github

from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
import os
import httpx
from tokens import decode_token,create_access_token
load_dotenv(".env")
app=FastAPI()

app.add_middleware(DBSessionMiddleware,db_url=os.environ["DATABASE_URL"])




oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f'https://github.com/login/oauth/authorize?client_id=${os.environ["GH_CLIENT_ID"]}&scope=repo',
    tokenUrl="https://github.com/login/oauth/access_token",
)
@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/github_login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={os.environ["GH_CLIENT_ID"]}&scope=repo',status_code=302)


@app.get("/github-auth")
async def github_code(code:str):
    params={
        'client_id':os.environ["GH_CLIENT_ID"],
        'client_secret':os.environ["GH_CLIENT_SECRET"],
        'code':code
    }

    headers={'Accept':'application/json'}
    async with httpx.AsyncClient() as client:
        response=await client.post(url="https://github.com/login/oauth/access_token",params=params,headers=headers)
    response_json=response.json()
    access_token=response_json['access_token']
    async with httpx.AsyncClient() as client:
        headers.update({'Authorization':f'Bearer {access_token}'})
        response=await client.get('https://api.github.com/user',headers=headers)
    created_token=create_access_token({'gh_access':access_token,'username':'test'})
    return {'token':created_token}

@app.get("/get_repos")
async def get_repos(token:str = Depends(decode_token)):
    try:

        g=Github(token)
        # for repo in g.get_user().get_repos():
        #     print(repo.owner.name)
        
            # print(dir(repo))
    except Exception as e:
        print (str(e))
    return [x.name for x in g.get_user().get_repos()]







if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
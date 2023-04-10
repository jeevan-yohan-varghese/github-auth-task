import uvicorn
from fastapi import FastAPI



from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
import os
load_dotenv(".env")
app=FastAPI()

app.add_middleware(DBSessionMiddleware,db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def root():
    return {"message":"Hello World"}



if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
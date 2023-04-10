from pydantic import BaseModel

class Repo(BaseModel):
    repo_id: str
    repo_name: str
    owner_id: str
    owner_name: str
    owner_email:str
    status: str
    stars: str
    
    
    

    class Config:
        orm_mode= True



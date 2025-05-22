from pydantic import BaseModel

class Signup(BaseModel):
    username : str
    email:str
    password:str
    role:str ='user'
    
class Signin(BaseModel):
    email : str
    password:str   
     
class Refresh_token(BaseModel):
    refresh_token:str    
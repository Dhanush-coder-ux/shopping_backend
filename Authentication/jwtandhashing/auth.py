from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,status

ACCESS_TOKEN_KEY="DFGHJKWFECDHJKJHVBN24y67983409-!@#$%^&*(MGW98UYEWUY"
REFRESH_TOKEN_KEY='2345678#$%^&*(dfghjmk<DFghjasklioel*(@#39u9*())'
ALGORITHM ="HS256"
ACCESS_TOKEN_EXP_TIME=30
REFRESH_TOKEN_DAY =7

def create_access_token( data:dict):
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXP_TIME)
    data['exp']=expire 
    acces_token= jwt.encode(data,key=ACCESS_TOKEN_KEY,algorithm=ALGORITHM)
    return acces_token


def create_refresh_token(data:dict):
    expire=datetime.now(timezone.utc)+timedelta(days=REFRESH_TOKEN_DAY)
    data['exp']=expire
    refresh_toke=jwt.encode(data,key=REFRESH_TOKEN_KEY,algorithm=ALGORITHM)
    return refresh_toke
    

def decode_jwt(toke:str,key:str):
    try:
       decoded_data=jwt.decode(token=toke,key=key,algorithms=ALGORITHM)
       return decoded_data
    except JWTError as e:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"error while verifiying {e}")
    
def get_access_token(refesh_token:str):
    to_decode =decode_jwt(refesh_token,REFRESH_TOKEN_KEY) 
    print(to_decode)
    new_access_token=create_access_token(to_decode)
    return new_access_token

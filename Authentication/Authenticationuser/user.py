from fastapi import FastAPI, Depends, HTTPException, status, APIRouter,Form
from database import schema, database
from Authentication.jwtandhashing import hashing, auth
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database.databasemodels import models
from database.depends import getdb



app = FastAPI()

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='/Signin')
router = APIRouter(tags=['UserAuthentication'])

@router.post('/Signup')
def sign_up(user: schema.Signup, db: Session = Depends(getdb.get_db)):
    Exist_user = db.query(models.User).filter(models.User.email == user.email).first()
    if Exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User Already Exists')

    try:
        hashed_password = hashing.hash_password(user.password)
        user_signup = models.User(
            username=user.username,
            email=user.email,
            password=hashed_password,
            role=user.role
        )
        db.add(user_signup)
        db.commit()
        db.refresh(user_signup)
        return {'message': f'{user.username}, you have successfully created an account as a {user.role}!'}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/Signin')
def sign_in(user: schema.Signin, db: Session = Depends(getdb.get_db)):
    login_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not login_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found Please sign up.')

    if not hashing.verify_password(user.password, login_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password')

    try:
        data = {'email': user.email}
        access_token = auth.create_access_token(data=data)
        refresh_token = auth.create_refresh_token(data=data)
        print("Generated Access Token:", access_token) 
        print("Generated Refresh Token:", refresh_token)
        
        return {'access_token': access_token, "refresh_token": refresh_token}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/new-accesstoken')
def new_access_token(new_ref: schema.Refresh_token):
    try:
        New_Access_Token = auth.get_access_token(new_ref.refresh_token)
        if not New_Access_Token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
        return {
            'New_Access_Token': New_Access_Token  
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    

# import os
# from dotenv import load_dotenv
# load_dotenv()
# ADMINE_EMAIL = os.getenv("ADMINE_EMAIL")
# ADMINE_PASSWORD = os.getenv("ADMINE_PASSWORD ")

ADMINE_EMAIL ="dhanushsubbia703@gmail.com"
ADMINE_PASSWORD ="Dhanush123"



@router.post('/admine')
def adminelogin(email: str = Form(...), password: str = Form(...), db: Session = Depends(getdb.get_db)):
   
    admin_user = db.query(models.User).filter(models.User.email == email).first()
    print('guuu')
    if not admin_user:
        if email == ADMINE_EMAIL and password == ADMINE_PASSWORD:
            hashed_password = hashing.hash_password(password)
            admin_user = models.User(username="Admin", email=email, password=hashed_password, role="admin")
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

 
    if email == ADMINE_EMAIL and password == ADMINE_PASSWORD:
        data = {'email': email}
        access_token = auth.create_access_token(data=data)
        refresh_token = auth.create_refresh_token(data=data)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')



           
@router.get('/protected')
def get_protected(
    token:str =Depends(oauth2_scheme),
    db:Session =Depends(getdb.get_db)
):
    try:
        print("qwertyuiol, bvcxawedfghjmb")
        print(token)
        decode_data = auth.decode_jwt(token,auth.ACCESS_TOKEN_KEY)
        print(decode_data)
        if not isinstance(decode_data,dict):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalide token')
        
        
        user = db.query(models.User).filter(models.User.email == decode_data.get("email")).first()
        print(user)
    
        if not user:
            raise HTTPException(status_code=404,detail='user not fount')

        return {'user':user.username,'email':user.email,'user_id':user.id,'role':user.role}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'error occured :{e}')



app.include_router(router)


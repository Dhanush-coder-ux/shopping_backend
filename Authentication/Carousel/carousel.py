from fastapi import FastAPI,HTTPException,Depends,UploadFile,APIRouter,File,status
from pydantic import BaseModel
from typing import List
from backend.database.depends.getdb import get_db
from sqlalchemy.orm import Session
from backend.Authentication.Authenticationuser.user import get_protected



router =APIRouter(tags=['Carousel route'])

router.post('/carousel')
def Carousel_Add_Banner(db:Session =Depends(get_db),Admin:dict=Depends(get_protected),
                        CarouselImage:List[UploadFile]=File(None)):
    if Admin["role"] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can add a carousel")
    
    pass
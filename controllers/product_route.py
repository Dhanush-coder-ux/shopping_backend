from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status,Response,Request
from sqlalchemy.orm import Session
from sqlalchemy import select,desc,func
from uuid import uuid4,uuid5
from backend.database.depends.getdb import get_db
from backend.database.databasemodels import product_models
from backend.Authentication.Authenticationuser.user import get_protected
from fastapi import APIRouter








router = APIRouter(tags=['ProductsController'])

 

@router.post('/add')
async def add_product(
    req:Request,
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(..., ge=0),  
    category: str = Form(...),
    subcategory: str = Form(...),
    sizes: str = Form(...),  
    bestseller: bool = Form(...),
    image1: UploadFile = File(None),
    image2: UploadFile = File(None),
    image3: UploadFile= File(None),
    image4: UploadFile = File(None),
    db: Session = Depends(get_db),
    admine: dict = Depends(get_protected)
):

    if admine["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Only admins can add products")

    existing_product = db.query(
        product_models.Product
        ).filter(product_models.Product.name == name
                 ).first()
    if existing_product:
        raise HTTPException(status_code=409, detail="Product Already Exists")
   
    try:
        product_id=str(uuid5(uuid4(),name))
        new_product = product_models.Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            category=category,
            subcategory=subcategory,
            sizes=sizes.strip().split(","),
            bestseller=bestseller,    
        )

        result=[] 
        images =[image1,image2,image3,image4]

        for image in images:
            imageid =str(uuid5(uuid4(),name))
            result.append(
                product_models.ProductImages(id=imageid,image=image.file.read(),product_id=product_id,image_url =f"{req.base_url}shop/product/image/{product_id}/{imageid}")
                )
    
        result.append(new_product)
        db.add_all(result)
        db.commit()
        return {'message': f'{new_product.name} has been added successfully!'}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    
 


@router.delete('/remove/{product_id}')
async def remove_product(product_id:str,db:Session=Depends(get_db),admine:dict =Depends(get_protected)):
    try:
        if admine["role"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can remove products")
        delete_product =db.query(product_models.Product
                                 ).filter(product_models.Product.id == product_id
                                          ).first()
        if not delete_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'this {product_id} Product Not Fount')
        print('delete')
        db.delete(delete_product)
        db.commit()
        return {'message':f'Product {delete_product.id} was deleted'}
    except HTTPException:
        raise    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Database error: {e}')        

    

@router.get('/single/{product_id}')
async def get_single_product(product_id:int,db:Session=Depends(get_db)):
    try:
        sing_product = db.query(product_models.Product
                                ).filter(product_models.Product.id == product_id
                                         ).first()
        if not sing_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{sing_product.id} is Not Found')
        return sing_product 
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))      
    
     

@router.get('/list')
async def list_all_products(db: Session = Depends(get_db)):
    try:
        products = db.execute(
            select(
                product_models.Product.id,
                product_models.Product.name,
                product_models.Product.description,
                product_models.Product.price,
                product_models.Product.category,
                product_models.Product.subcategory,
                product_models.Product.sizes,
                product_models.Product.bestseller,
                func.array_agg(product_models.ProductImages.image_url).label("images")
            ).join(product_models.ProductImages,isouter=True,full=True)
            .group_by(
                product_models.Product.id,
                product_models.Product.name,
                product_models.Product.description,
                product_models.Product.price,
                product_models.Product.category,
                product_models.Product.subcategory,
                product_models.Product.sizes,
                product_models.Product.bestseller
            )
        ).mappings().all()
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


@router.get('/shop/product/image/{product_id}/{imageid}')
def get_img(product_id:str,imageid:str,db: Session = Depends(get_db)):
    _get_img=db.query(
        product_models.ProductImages
        ).filter(product_models.ProductImages.id == imageid,product_models.ProductImages.product_id == product_id
                 ).first()
    if not _get_img:
        raise HTTPException(status_code=404)
    return Response(_get_img.image,media_type='image/jpg')




from fastapi import FastAPI, APIRouter, Depends, HTTPException
from backend.Authentication.Authenticationuser.user import get_protected
from backend.database.databasemodels.models import Cart
from backend.database.depends import getdb
from backend.database.databasemodels import product_models
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from pydantic import BaseModel
from icecream import ic

router = APIRouter(tags=["Cart"])




class AddToCartSchema(BaseModel):
    product_id: str
    size: str
    quantity:int= 1 

@router.post("/add-cart")
def add_to_cart(cart: AddToCartSchema, db: Session = Depends(getdb.get_db), current_user:dict=Depends(get_protected)):
    ic("hiiii")
    existing_item = db.query(Cart).filter_by(
        user_id=current_user["user_id"],
        product_id=cart.product_id,
        size=cart.size
    ).first()

    if existing_item:
        raise HTTPException(
            status_code=409,
            detail="product already exists"
        )
    new_item = Cart(
            user_id=current_user["user_id"],
            product_id=cart.product_id,
            size=cart.size,
            quantity=cart.quantity
        )
    db.add(new_item)
    db.commit()
    return {"message": "Product added to cart successfully!"}


@router.get('/get-cart')
async def user_cart(user: dict = Depends(get_protected), db: Session = Depends(getdb.get_db)):
    cart_item = db.execute(
        select(
            product_models.Product.id,
            product_models.Product.name,
            product_models.Product.price,
            Cart.size,
            Cart.quantity,
            func.array_agg(product_models.ProductImages.image_url).label("images")
        )
        .select_from(Cart)
        .join(product_models.Product, Cart.product_id == product_models.Product.id)
        .outerjoin(product_models.ProductImages, product_models.ProductImages.product_id == product_models.Product.id)
        .where(Cart.user_id == user["user_id"])
        .group_by(
            product_models.Product.id,
            product_models.Product.name,
            product_models.Product.price,
            Cart.size,
            Cart.quantity
        )
    ).mappings().all()

    if not cart_item:
        return {"message": "Your Cart is Empty"}
    
    return {"cartdata": cart_item}

 


    
@router.put('/update-cart')
async def update_cart(cart: AddToCartSchema,user:dict=Depends(get_protected),db:Session=Depends(getdb.get_db)):
    existing_item = db.query(Cart).filter_by(
        user_id=user["user_id"],
        product_id=cart.product_id,
        size=cart.size
    ).first()

    if existing_item:
        existing_item.quantity = cart.quantity
    else:
        new_item = Cart(
            user_id=user["user_id"],
            product_id=cart.product_id,
            size=cart.size,
            quantity=cart.quantity
        )
        db.add(new_item)
    db.commit()
    return {"message": "Updated Cart successfully!"}


@router.delete('/delete-cart')
async def delete_cart(cart: AddToCartSchema, db: Session = Depends(getdb.get_db), user: dict = Depends(get_protected)):
    delete_item = db.query(Cart).filter_by(
        user_id=user["user_id"],
        product_id=cart.product_id,
        size=cart.size
    ).first()

    if not delete_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(delete_item)
    db.commit()
    return {"message": "Product deleted from cart successfully!"}
 


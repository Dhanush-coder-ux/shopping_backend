from fastapi import APIRouter,Depends,HTTPException,status
from database.depends import getdb
from sqlalchemy.orm import Session
from Authentication.Authenticationuser.user import get_protected
from pydantic import BaseModel
from typing import List
from database.databasemodels.order_model import Orders,OrderStatus
from icecream import ic

router=APIRouter(tags=["Orders"])

class ProductItem(BaseModel):
    id: str
    name: str
    category: str
    subcategory: str
    description: str
    price: int
    quantity: int
    size: str
    images: List[str]
    bestseller: bool

    

class OrderCreate(BaseModel):
    products: List[ProductItem]
    amount: int
    address: List[str]
    paymentmethod: str

class UpdateStatusRequest(BaseModel):
    order_id: int
    new_status: OrderStatus


# payment features
@router.post('/placeorders')
def place_order(order: OrderCreate, db: Session = Depends(getdb.get_db), current_user: dict = Depends(get_protected)):
    ic(order)
    try:
        products_serialized = [item.dict() for item in order.products]
        new_order = Orders(
            user_id=current_user["user_id"],
            products=products_serialized,
            amount=order.amount,
            address=order.address,
            paymentmethod=order.paymentmethod,
            payment=False
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return {"message": "Order placed successfully"}
    except Exception as e:
        ic(f"error :{e}")
        raise HTTPException(status_code=500,detail="internal server error")


@router.post('/stripepay')
def place_OrderStripe(db: Session = Depends(getdb.get_db),):
    pass
@router.post('/razorpay')
def placeOrderRazor(db: Session = Depends(getdb.get_db),):
    pass


# Admin features
@router.post('/allorders')
def allOrders(db: Session = Depends(getdb.get_db),admine:dict = Depends(get_protected)):
    if admine["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Only admin")
    all_Orders =db.query(Orders).all()
    return{"allOrders":all_Orders}

@router.put('/update-status')
def update_Status(status_update:UpdateStatusRequest,db: Session = Depends(getdb.get_db),admine:dict = Depends(get_protected)):
    
    if admine['role'] != "admin":
        raise HTTPException(
            status_code=403,detail="only admine can update"
        )
    
    order_item= db.query(Orders).filter(
        Orders.id == status_update.order_id
    ).first()


    if not order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {status_update.order_id} not found")

    order_item.status =status_update.new_status
    db.commit()
    return {"message": "Order status updated successfully"}







# User features
@router.post('/userorders')
def user_Orders(db: Session = Depends(getdb.get_db),current_user: dict = Depends(get_protected)):
    user_Orders_item=db.query(Orders).filter(Orders.user_id == current_user["user_id"]).all()

    if not user_Orders_item:
        raise HTTPException(status_code=401,detail="Your Order Is Empty")
    return{'OrderItems':user_Orders_item}
    
   
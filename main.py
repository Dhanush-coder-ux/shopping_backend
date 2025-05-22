from fastapi import FastAPI
from Authentication.Authenticationuser import user
from controllers import cart_route
from controllers import product_route
from controllers import order_controls
from database.databasemodels import models
from database import database



app= FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel"}


from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 


)

models.Base.metadata.create_all(bind=database.engine)
app.include_router(user.router)
app.include_router(product_route.router)
app.include_router(cart_route.router,prefix="/cart")
app.include_router(order_controls.router,prefix="/orders")
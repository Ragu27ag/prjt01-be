from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    user_name : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    mobile_number : Optional[str] = None
    profile_picture : Optional[str] = None
    user_id : Optional[str] = None
    customer_type : Optional[str] = None
    proof_of_verification : Optional[str] = None
    gender : Optional[str] = None 

class UserPost(BaseModel):
    user_id : str
    post_type : str
    post_url : Optional[str]
    post_description : Optional[str]
    market_id : Optional[str] = None

class GetUserPost(BaseModel):
    user_id : Optional[str] = None
    market_id : Optional[str] = None

class PostLikes(BaseModel):
    post_id : Optional[str] = None
    user_id : Optional[str] = None  

class PostComments(BaseModel):
    post_id : Optional[str] = None 
    user_id :Optional[str] = None   
    comment : Optional[str] = None 

class ProductsRequest(BaseModel):
    user_id :Optional[str] = None  
    product_name : Optional[str] = None
    product_description : Optional[str] = None
    manufacturer_name : Optional[str] = None
    manufacturer_address : Optional[str] = None
    product_image_url : Optional[str] = None
    product_price : Optional[float] = None
    stocks : Optional[float] = None
    product_id : Optional[str] = None
    market_id : Optional[str] = None

class ProductsRatingRequest(BaseModel):
    user_id :Optional[str] = None  
    product_id : Optional[str] = None
    star_rating : Optional[str] = None
    comments : Optional[str] = None

class MarketRequest(BaseModel):
    user_id :Optional[str] = None  
    market_name : Optional[str] = None
    market_description : Optional[str] = None
    market_address : Optional[str] = None
    market_image_url : Optional[str] = None
    market_id :Optional[str] = None


class OrdersRequest(BaseModel):
    user_id : Optional[str] = None
    customer_name : Optional[str] = None
    product_name : Optional[str] = None 
    product_image_url : Optional[str] = None
    product_price : Optional[float] = None
    quantity : Optional[float] = None
    product_id : Optional[str] = None
    market_id : Optional[str] = None
    billing_address : Optional[str] = None
    date_of_delivery : Optional[str] = None
    order_status : Optional[str] = None
    order_id : Optional[str] = None
    
class ImageData(BaseModel) :
    image_url : str
    



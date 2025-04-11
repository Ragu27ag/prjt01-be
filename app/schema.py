from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    user_name : Optional[str]
    email : str
    password : str
    mobile_number : Optional[str]
    profile_picture : Optional[str]

class UserPost(BaseModel):
    user_id : str
    post_type : str
    post_url : Optional[str]
    post_description : Optional[str]

class GetUserPost(BaseModel):
    user_id : Optional[str]

class PostLikes(BaseModel):
    post_id : str
    user_id :Optional[str]    

class PostComments(BaseModel):
    post_id : str
    user_id :Optional[str]  
    comment : Optional[str]

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

class ProductsRatingRequest(BaseModel):
    user_id :Optional[str]  
    product_id : Optional[str]
    star_rating : Optional[str]
    comments : Optional[str]



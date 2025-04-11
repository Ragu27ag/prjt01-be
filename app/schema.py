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
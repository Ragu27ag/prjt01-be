import json
from typing import Dict
from uuid import uuid4
import aiomysql
from passlib.context import CryptContext
from app.schema import GetUserPost, UserPost, UserRequest


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_users(user_body : UserRequest,db_pool) -> Dict[str,str] :
    
    email = user_body.email
    select_query = """
    SELECT *
        FROM users
        WHERE email = %s
    """

    async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(select_query, (email,))
                row = await cursor.fetchone()
    print('row',row)
    if len(row) > 0 :
        return {'error' : 'User Already Exist','data': None}
    
    user_id = str(uuid4())
    print('user id',user_id)
    hashed_password = hash_password(user_body.password)
    
    query = """
    INSERT INTO users (id, user_name, email, password, mobile_number, profile_picture)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (user_id,user_body.user_name,user_body.email,hashed_password,user_body.mobile_number,user_body.profile_picture)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None}
    

async def login_user(user_body : UserRequest,db_pool) -> Dict[str,str] : 

    query = """
    SELECT *
        FROM users
        WHERE email = %s
    """
    email = user_body.email
    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (email,))
                row = await cursor.fetchone()

        ver = verify_password(user_body.password,row[3])

        if(ver) :
            val = {
                    "id": row[0],
                    "user_name": row[1],
                    "email": row[2],
                    "mobile_number": row[4],
                    "profile_picture": row[5],
            }
            return {'error' : None,'data': json.dumps(val)}
        else : 
            return {'error' : 'Invalid Password' ,'data': None}
    except Exception as e:
        return {'error' : str(e),'data': None}
    

async def user_post(user_body : UserPost,db_pool) -> Dict[str,str] : 

    post_id = str(uuid4())
    print('user id',post_id)
    
    query = """
    INSERT INTO posts (post_id,user_id,post_type ,post_url,post_description)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (post_id,user_body.user_id,user_body.post_type,user_body.post_url,user_body.post_description)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None}  
    

async def get_user_post(user_body : GetUserPost,db_pool) -> Dict[str,str] : 

    query = None

    if user_body.user_id is None :
        query = """
        SELECT post_id,user_id,post_type ,post_url,post_description, DATE_FORMAT(created_at, '%%Y-%%m-%%dT%%H:%%i:%%s') AS created_at
         FROM posts
        """
    else :
         query = """
        SELECT post_id,user_id,post_type ,post_url,post_description, DATE_FORMAT(created_at, '%%Y-%%m-%%dT%%H:%%i:%%s') AS created_at
        FROM posts where user_id = %s
        """

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                if user_body.user_id is not None :
                    await cursor.execute(query, (user_body.user_id,))
                    row = await cursor.fetchall()
                else :
                    await cursor.execute(query)
                    row = await cursor.fetchall()
    
        print('row',row)
                
        return {'error' : None,'data': row}
    except Exception as e:
        return {'error' : str(e),'data': None}  
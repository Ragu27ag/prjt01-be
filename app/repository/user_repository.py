import json
from typing import Dict
from uuid import uuid4
import aiomysql
from passlib.context import CryptContext
from app.schema import GetUserPost, PostComments, PostLikes, UserPost, UserRequest


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
    if row is not None :
        return {'error' : 'Email already exists','data': None}
    
    user_id = str(uuid4())
    print('user id',user_id)
    hashed_password = hash_password(user_body.password)
    
    query = """
    INSERT INTO users (user_id, user_name, email, password, mobile_number, profile_picture,customer_type,proof_of_verification,gender)
    VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)
    """

    values = (user_id,user_body.user_name,user_body.email,hashed_password,user_body.mobile_number,user_body.profile_picture,user_body.customer_type,user_body.proof_of_verification,user_body.gender)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)

        select_query = """
        SELECT *
        FROM users
        WHERE email = %s
    """

        async with db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(select_query, (email,))
                    row = await cursor.fetchall()
                
        return {'error' : None,'data': row}
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
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (email,))
                row = await cursor.fetchall()

                print('row',row)

                if not row :
                    return {'error' : "User doesn't exist. Signup to continue" ,'data': None}

        ver = verify_password(user_body.password,row[0]['password'])

        if ver :
            return {'error' : None,'data': row}
        else : 
             return {'error' : 'Invalid Password' ,'data': None}
    except Exception as e:
        return {'error' : str(e),'data': None}
    

async def get_user(user_body : UserRequest,db_pool) -> Dict[str,str] : 

    query = """
    SELECT *
        FROM users
        WHERE user_id = %s
    """
    
    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (user_body.user_id,))
                row = await cursor.fetchall()

                print('row',row)

            return {'error' : None,'data': row}
       
    except Exception as e:
        return {'error' : str(e),'data': None}
    

async def user_post(user_body : UserPost,db_pool) -> Dict[str,str] : 

    post_id = str(uuid4())
    print('user id',post_id)
    
    query = """
    INSERT INTO posts (post_id,user_id,post_type ,post_url,post_description,market_id)
    VALUES (%s, %s, %s, %s, %s,%s)
    """

    values = (post_id,user_body.user_id,user_body.post_type,user_body.post_url,user_body.post_description,user_body.market_id)

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
        SELECT post_id,user_id,post_type ,post_url,post_description, DATE_FORMAT(created_at, '%d/%m/%y %H:%i:%s')  AS created_at
         FROM posts
        """
    else :
         query = """
        SELECT post_id,user_id,post_type ,post_url,post_description, DATE_FORMAT(created_at, '%d/%m/%y %H:%i:%s')  AS created_at
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
    

async def post_likes(user_body : PostLikes,db_pool) -> Dict[str,str] :

    select_query = """
    SELECT *
        FROM post_likes where user_id = %s and post_id = %s
    """ 
    try:
        async with db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(select_query, (user_body.user_id, user_body.post_id))
                        row = await cursor.fetchall()
        print('row',row)
        if row  :
            delete_query = """
            delete
                FROM post_likes where user_id = %s and post_id = %s
            """  
            async with db_pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(delete_query, (user_body.user_id, user_body.post_id))
            return {'error' : None,'data': user_body}
    except Exception as e:
        print('e',e)
    
    
    
    query = """
    INSERT INTO post_likes (post_id,user_id)
    VALUES (%s, %s)
    """

    values = (user_body.post_id,user_body.user_id)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 


async def get_post_likes(user_body : PostLikes,db_pool) -> Dict[str,str] : 
    query = """
    SELECT *
        FROM post_likes where  user_id = %s
    """

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, (user_body.user_id,))
                    row = await cursor.fetchall()
    
        print('row',row)
                
        return {'error' : None,'data': row}
    except Exception as e:
        return {'error' : str(e),'data': None}   
    

async def get_post_likes_count(user_body : PostLikes,db_pool) -> Dict[str,str] : 
    query = """
    SELECT *
        FROM post_likes where post_id = %s 
    """

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, (user_body.post_id,))
                    row = await cursor.fetchall()
    
        print('row',row)
                
        return {'error' : None,'data': row}
    except Exception as e:
        return {'error' : str(e),'data': None}   
    

async def post_comments(user_body : PostComments,db_pool) -> Dict[str,str] : 
    
    query = """
    INSERT INTO post_comments (post_id,user_id,comments)
    VALUES (%s, %s, %s)
    """

    values = (user_body.post_id,user_body.user_id,user_body.comment)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 


async def get_post_comment(user_body : PostComments,db_pool) -> Dict[str,str] : 
    query = """
    SELECT *
        FROM post_comments where post_id = %s
    """

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, (user_body.post_id,))
                    row = await cursor.fetchall()
    
        print('row',row)
                
        return {'error' : None,'data': row}
    except Exception as e:
        return {'error' : str(e),'data': None}  
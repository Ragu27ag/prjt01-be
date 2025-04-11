from contextlib import asynccontextmanager
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import aiomysql
import asyncio
from dotenv import load_dotenv
import os
from uuid import uuid4
from app.repository.product_repository import add_products, add_products_ratings, get_products, get_products_ratings, remove_products, update_products
from app.repository.user_repository import create_users, get_post_comment, get_post_likes, get_user_post, login_user, post_comments, post_likes, user_post
from fastapi.responses import JSONResponse, ORJSONResponse



from app.schema import GetUserPost, PostComments, PostLikes, ProductsRatingRequest, ProductsRequest, UserPost, UserRequest
load_dotenv()


db_connection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
    db_pool = await aiomysql.create_pool(
        host=os.getenv('DB_HOST'),
        port=3306,
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        autocommit=True,
        maxsize=10  # Maximum connections in the pool
    )
    try:
        # Test DB connection with a simple query
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT 1")
                result = await cursor.fetchone()
                if result and result[0] == 1:
                    print("✅ Database connection verified")
                else:
                    print("⚠️  Unexpected response from DB")
    except Exception as e:
        print("❌ Failed to connect to DB:", str(e))
    yield


app = FastAPI(title="Prjt-01",
    description="Prjt-01 Server",
    version="1.0.0",
    lifespan=lifespan)






@app.get('/api/v1/health')
def health():
   return 'Up and On'


@app.post('/api/v1/addusers')
async def addUser(user_body : UserRequest):
    
    res = await create_users(user_body,db_pool)

    print('res',res)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "User added",
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )
    
@app.post('/api/v1/login_user')
async def login(user_body:UserRequest) :
    res = await login_user(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Login success",
            "data" : json.loads(res['data'])
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/add-post')
async def add_post(user_body:UserPost) :
    res = await user_post(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Post Added Successfully",
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/get-post')
async def get_post(user_body:GetUserPost) :
    res = await get_user_post(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":res['data']
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/add-post-likes')
async def add_post_likes(user_body:PostLikes) :
    res = await post_likes(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts"
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/get-post-likes')
async def get_posts_likes(user_body:PostLikes) :
    res = await get_post_likes(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":res['data']
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )


@app.post('/api/v1/post-comments')
async def add_post_comments(user_body:PostComments) :
    res = await post_comments(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/get-post-comments')
async def get_post_comments(user_body:PostComments) :
    res = await get_post_comment(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":res['data']
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/add-product')
async def add_product(user_body:ProductsRequest) :
    res = await add_products(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts"
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/update-product')
async def update_product(user_body:ProductsRequest) :
    res = await update_products(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts"
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/delete-product')
async def delete_product(user_body:ProductsRequest) :
    res = await remove_products(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":res['data']
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/get-products')
async def get_product(user_body:ProductsRequest) :
    res = await get_products(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":res['data']
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )


@app.post('/api/v1/add-product-rating')
async def add_product_rating(user_body:ProductsRatingRequest) :
    res = await add_products_ratings(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts"
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )

@app.post('/api/v1/get-product-rating')
async def get_product_rating(user_body:ProductsRatingRequest) :
    res = await get_products_ratings(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":res['data']
        }
    )
    else : 
      return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInput",
            "message": res['error'],
        }
    )




@app.get('/api/v1/create-tables')
async def create_tables():
    tables = {
        'users' : '''create table if not exists users (user_id CHAR(36) PRIMARY KEY,user_name VARCHAR(100) , email VARCHAR(100) , password VARCHAR(100) , mobile_number VARCHAR(10) , profile_picture VARCHAR(1000))''',
        'posts' : '''create table if not exists posts (post_id CHAR(36) PRIMARY KEY, user_id CHAR(36),post_type VARCHAR(20) , post_url VARCHAR(1000),post_description VARCHAR(10000),created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
        'post_likes' : '''create table if not exists post_likes (post_id CHAR(36) PRIMARY KEY, user_id CHAR(36))''',
        'post_comments' : '''create table if not exists post_comments (post_id CHAR(36) PRIMARY KEY, user_id CHAR(36),comments VARCHAR(10000))''',
        'products' : '''create table if not exists products (product_id CHAR(36) PRIMARY KEY, user_id CHAR(36),product_name VARCHAR(200),product_description VARCHAR(10000),manufacturer_name VARCHAR(200),manufacturer_address VARCHAR(2000),product_image_url VARCHAR(2000),product_price INTEGER,stocks INTEGER,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
        'products_ratings' : '''create table if not exists products_ratings (product_id CHAR(36) PRIMARY KEY, user_id CHAR(36),star_rating VARCHAR(20),comments VARCHAR(10000))'''

    }
    
    async with db_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                for table_name in tables :
                    table_details = tables[table_name]
                    await cursor.execute(table_details)
    
    
    return 'Successfully created'




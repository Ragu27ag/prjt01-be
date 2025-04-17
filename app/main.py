from contextlib import asynccontextmanager
import json
from app.service.ocrservice import identify_gender
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import aiomysql
import asyncio
from dotenv import load_dotenv
import os
from uuid import uuid4
from app.repository.market_repository import add_market, get_market, update_market
from app.repository.orders_repository import add_orders, get_orders, update_orders
from app.repository.product_repository import add_products, add_products_ratings, get_products, get_products_ratings, remove_products, update_products
from app.repository.user_repository import create_users, get_post_comment, get_post_likes, get_post_likes_count, get_user, get_user_post, login_user, post_comments, post_likes, user_post
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware




from app.schema import GetUserPost, ImageData, MarketRequest, OrdersRequest, PostComments, PostLikes, ProductsRatingRequest, ProductsRequest, UserPost, UserRequest
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






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
            "message": "Inserted Successfully",
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
    
@app.post('/api/v1/login-user')
async def login(user_body:UserRequest) :
    res = await login_user(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Login success",
            "data" : res['data']
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
            "message": "Inserted Successfully",
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
    final_res = []
    for posts in res['data'] :
       print('posts',posts)
       final_dict = {}
       market = await get_market(MarketRequest(user_id=posts['user_id']), db_pool)
       post_likes = await get_post_likes_count(PostLikes(post_id=posts['post_id']), db_pool)
       comments = await get_post_comment(PostComments(post_id=posts['post_id']), db_pool)
       print('market',market)
       if market['data'] :
        final_dict = {**posts,**market['data'][0]}
       else :
        final_dict = {**posts}

       final_dict['likes_count'] = len(post_likes['data']) | 0
       final_dict['comments_count'] = len(comments['data']) | 0
       final_res.append(final_dict)

    print('final_res',final_res)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":final_res
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
            "message": "Liked Successfully"
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

    final_res = []
    for posts in res['data'] :
       print('posts',posts)
       final_dict = {}
       comments = await get_user(UserRequest(user_id=posts['user_id']), db_pool)
       
       final_dict = {**posts,**comments['data'][0]}

       final_res.append(final_dict)

    print('final_res',final_res)


    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Comments",
            "data":final_res
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
            "message": "Inserted Successfully"
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

    final_res = []
    for products in res['data'] :
       print('products',products)
       final_dict = {}
       ratings = await get_products_ratings(ProductsRatingRequest(product_id=products['product_id']), db_pool)
       print('ratings',ratings)
       if ratings['data'] :
        final_dict = {**products,**ratings['data'][0]}
       else :
        final_dict = {**products}

       final_res.append(final_dict)

    print('final_res',final_res)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data": final_res
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


@app.post('/api/v1/add-market')
async def add_markets(user_body:MarketRequest) :
    res = await add_market(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Inserted Successfully"
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

@app.post('/api/v1/update-market')
async def update_markets(user_body:MarketRequest) :
    res = await update_market(user_body,db_pool)

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


@app.post('/api/v1/get-market')
async def get_markets(user_body:MarketRequest) :
    res = await get_market(user_body,db_pool)

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


@app.post('/api/v1/add-order')
async def add_order(user_body:OrdersRequest) :
    res = await add_orders(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Inserted Successfully"
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

@app.post('/api/v1/update-order')
async def update_order(user_body:OrdersRequest) :
    res = await update_orders(user_body,db_pool)

    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Updated Successfully"
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


@app.post('/api/v1/get-order')
async def get_order(user_body:OrdersRequest) :
    res = await get_orders(user_body,db_pool)


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
      
      
@app.post('/api/v1/validate-proof')
async def get_order(imageData : ImageData) :
    res = await identify_gender(imageData)


    if res['error'] is None :
       return JSONResponse(
        status_code=200,
        content={
            "message": "Posts",
            "data":res
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
        'users' : '''create table if not exists users (user_id CHAR(36) PRIMARY KEY,user_name VARCHAR(100) , email VARCHAR(100) , password VARCHAR(100) , mobile_number VARCHAR(10) , profile_picture VARCHAR(1000) ,,customer_type VARCHAR(1000),proof_of_verification VARCHAR(2000),gender VARCHAR(10))''',
        'posts' : '''create table if not exists posts (post_id CHAR(36) PRIMARY KEY, user_id CHAR(36),market_id CHAR(36),post_type VARCHAR(20) , post_url VARCHAR(1000),post_description VARCHAR(10000),created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
        'post_likes' : '''create table if not exists post_likes (post_id CHAR(36), user_id CHAR(36),market_id CHAR(36))''',
        'post_comments' : '''create table if not exists post_comments (post_id CHAR(36), user_id CHAR(36),market_id CHAR(36),comments VARCHAR(10000))''',
        'products' : '''create table if not exists products (product_id CHAR(36) PRIMARY KEY, user_id CHAR(36),market_id CHAR(36),product_name VARCHAR(200),product_description VARCHAR(10000),manufacturer_name VARCHAR(200),manufacturer_address VARCHAR(2000),product_image_url VARCHAR(2000),product_price INTEGER,stocks INTEGER,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
        'products_ratings' : '''create table if not exists products_ratings (product_id CHAR(36), user_id CHAR(36),market_id CHAR(36),star_rating VARCHAR(20),comments VARCHAR(10000))''',
        'market' : '''create table if not exists market (market_id CHAR(36) PRIMARY KEY, user_id CHAR(36),market_name VARCHAR(200),market_description VARCHAR(10000),market_address VARCHAR(2000),market_image_url VARCHAR(2000))''',
        'orders' : '''create table if not exists orders (product_id CHAR(36), user_id CHAR(36),market_id CHAR(36),order_id CHAR(36) PRIMARY KEY,product_name VARCHAR(200),customer_name VARCHAR(200),product_image_url VARCHAR(2000),product_price INTEGER,quantity INTEGER,billing_address VARCHAR(2000),date_of_delivery VARCHAR(200),order_status VARCHAR(200),created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    }
    
    async with db_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                for table_name in tables :
                    table_details = tables[table_name]
                    await cursor.execute(table_details)
    
    
    return 'Successfully created'




from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import aiomysql
import asyncio
from dotenv import load_dotenv
import os
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
    print('Database pool created')
    yield


app = FastAPI(title="Prjt-01",
    description="Prjt-01 Server",
    version="1.0.0",
    lifespan=lifespan)




@app.get('/api/v1/health')
def health():
   return 'Up and On'


@app.post('/api/v1/addusers')
def addUser():
    return


@app.get('/api/v1/create-tables')
async def create_tables():
    tables = {
        'users' : '''create table if not exists users (id CHAR(36) PRIMARY KEY,user_name VARCHAR(100) , email VARCHAR(100) , password VARCHAR(100) , mobile_number VARCHAR(10) , profile_picture VARCHAR(1000))'''
    }
    
    
    async with db_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                for table_name in tables :
                    table_details = tables[table_name]
                    await cursor.execute(table_details)
    
    
    return 'Successfully created'




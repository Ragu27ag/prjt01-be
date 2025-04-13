from typing import Dict
from uuid import uuid4
import aiomysql
from app.schema import MarketRequest



async def add_market(user_body : MarketRequest,db_pool) -> Dict[str,str] : 
    market_id = str(uuid4())
    query = """
    INSERT INTO market (market_id,user_id ,
    market_name ,
    market_description ,
    market_address ,
    market_image_url)
    VALUES (%s, %s, %s,%s, %s, %s)
    """

    values = (market_id,user_body.user_id,user_body.market_name,user_body.market_description,user_body.market_address,user_body.market_image_url)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 


async def update_market(user_body : MarketRequest,db_pool) -> Dict[str,str] : 
    query = f"""
    update products
    """

    if user_body.market_name is not None :
        query += f""" set market_name = '{user_body.market_name}'"""
    if user_body.market_description is not None :
        query += f""" set market_description = '{user_body.market_description}'"""
    if user_body.market_address is not None :
        query += f""" set market_address = '{user_body.market_address}'"""
    if user_body.market_image_url is not None :
        query += f""" set market_image_url = '{user_body.market_image_url}'"""
    
    query += f""" where product_id = '{user_body.market_id}' and user_id = '{user_body.user_id}'"""

    print('query',query)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 
    

async def get_market(user_body : MarketRequest,db_pool) -> Dict[str,str] : 
    query = None
    if user_body.user_id is None :
        query = """
        SELECT *
         FROM market
        """
    else :
         query = """
        SELECT *
        FROM market where user_id = %s
        """

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                if user_body.user_id is not None :
                    await cursor.execute(query, (user_body.user_id))
                    row = await cursor.fetchall()
                else :
                    await cursor.execute(query)
                    row = await cursor.fetchall()
    
        print('row',row)
        
        if row :
            return {'error' : None,'data': row}
        else :
            return {'error' : None,'data': []}
    except Exception as e:
        return {'error' : str(e),'data': None} 
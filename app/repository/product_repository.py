from typing import Dict
from uuid import uuid4
import aiomysql
from app.schema import ProductsRatingRequest, ProductsRequest



async def add_products(user_body : ProductsRequest,db_pool) -> Dict[str,str] : 
    product_id = str(uuid4())
    query = """
    INSERT INTO products (product_id,user_id ,
    product_name ,
    product_description ,
    manufacturer_name ,
    manufacturer_address ,
    product_image_url ,
    product_price ,
    stocks,market_id )
    VALUES (%s, %s, %s,%s, %s, %s,%s, %s,%s,%s)
    """

    values = (product_id,user_body.user_id,user_body.product_name,user_body.product_description,user_body.manufacturer_name,user_body.manufacturer_address,user_body.product_image_url,user_body.product_price,user_body.stocks,user_body.market_id)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 


async def update_products(user_body : ProductsRequest,db_pool) -> Dict[str,str] : 
    query = f"""
    update products set
    """

    if user_body.product_name is not None :
        query += f"""  product_name = '{user_body.product_name}',"""
    if user_body.product_description is not None :
        query += f"""  product_description = '{user_body.product_description}',"""
    if user_body.manufacturer_name is not None :
        query += f"""  manufacturer_name = '{user_body.manufacturer_name}',"""
    if user_body.manufacturer_address is not None :
        query += f"""  manufacturer_address = '{user_body.manufacturer_address}',"""
    if user_body.product_image_url is not None :
        query += f"""  product_image_url = '{user_body.product_image_url}',"""
    if user_body.product_price is not None :
        query += f"""  product_price = '{user_body.product_price}',"""
    if user_body.stocks is not None :
        query += f"""  stocks = '{user_body.stocks}'"""
    
    query += f""" where product_id = '{user_body.product_id}'"""

    print('query',query)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 
    

async def remove_products(user_body : ProductsRequest,db_pool) -> Dict[str,str] : 
    query = f"""
    delete products where product_id = {user_body.product_id} and user_id = {user_body.user_id}
    """

    print('query',query)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 


async def get_products(user_body : ProductsRequest,db_pool) -> Dict[str,str] : 
    query = None

    if user_body.user_id is None :
        query = """
        SELECT product_id,user_id ,market_id,
        product_name ,
        product_description ,
        manufacturer_name ,
        manufacturer_address ,
        product_image_url ,
        product_price ,
        stocks, DATE_FORMAT(created_at, '%%Y-%%m-%%dT%%H:%%i:%%s') AS created_at
         FROM products
        """
    else :
         query = """
        SELECT product_id,user_id ,market_id,
        product_name ,
        product_description ,
        manufacturer_name ,
        manufacturer_address ,
        product_image_url ,
        product_price ,
        stocks, DATE_FORMAT(created_at, '%%Y-%%m-%%dT%%H:%%i:%%s') AS created_at
        FROM products where user_id = %s
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
    

async def get_products_by_product_id(user_body : ProductsRequest,db_pool) -> Dict[str,str] : 
    

   
    query = """
        SELECT product_id,user_id ,
        product_name ,
        product_description ,
        manufacturer_name ,
        manufacturer_address ,
        product_image_url ,
        product_price ,
        stocks, DATE_FORMAT(created_at, '%%Y-%%m-%%dT%%H:%%i:%%s') AS created_at
         FROM products where product_id = %s
        """
   

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
              
                    await cursor.execute(query, (user_body.product_id,))
                    row = await cursor.fetchall()
             
    
        print('row',row)
                
        return {'error' : None,'data': row}
    except Exception as e:
        return {'error' : str(e),'data': None}  
    

async def add_products_ratings(user_body : ProductsRatingRequest,db_pool) -> Dict[str,str] : 

    select_query = """
        SELECT *
            FROM products_ratings where product_id = %s and user_id = %s
        """

        
    async with db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(select_query, (user_body.product_id,user_body.user_id,))
                        row = await cursor.fetchall()
        
    print('row',row)

    if row is not None :
        delete_query = """ delete
            FROM products_ratings where product_id = %s and user_id = %s"""
        
        async with db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(delete_query, (user_body.product_id,user_body.user_id,))
                        row = await cursor.fetchall()



    query = """
    INSERT INTO products_ratings (product_id,user_id ,
    star_rating,
    comments )
    VALUES (%s, %s, %s,%s)
    """

    values = (user_body.product_id,user_body.user_id,user_body.star_rating,user_body.comments)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None}
    

async def get_products_ratings(user_body : ProductsRatingRequest,db_pool) -> Dict[str,str] : 
    query = None

    if user_body.user_id is None :
        query = """
        SELECT *
         FROM products_ratings where product_id = %s
        """
    else :
         query = """
        SELECT *
        FROM products_ratings where product_id = %s  and user_id = %s 
        """
         
         print('query',query)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                if user_body.user_id is  None :
                    await cursor.execute(query, (user_body.product_id,))
                    row = await cursor.fetchall()
                else :
                    await cursor.execute(query, (user_body.product_id,user_body.user_id,))
                    row = await cursor.fetchall()
    
        print('row',row)
                
        return {'error' : None,'data': row}
    except Exception as e:
        return {'error' : str(e),'data': None}  
    


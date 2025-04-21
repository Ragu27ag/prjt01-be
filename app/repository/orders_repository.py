from typing import Dict
from uuid import uuid4
import aiomysql
from app.schema import OrdersRequest



async def add_orders(user_body : OrdersRequest,db_pool) -> Dict[str,str] : 
    order_id = str(uuid4())
    query = """
    INSERT INTO orders (order_id,user_id ,
    customer_name,
    product_name,
    product_image_url,
    product_price,
    quantity,
    product_id,
    market_id,
    billing_address,
    date_of_delivery,
    order_status )
    VALUES (%s, %s, %s,%s, %s, %s,%s, %s,%s,%s,%s,%s)
    """

    values = (order_id,user_body.user_id,user_body.customer_name,user_body.product_name,user_body.product_image_url,user_body.product_price,user_body.quantity,user_body.product_id,user_body.market_id,user_body.billing_address,user_body.date_of_delivery,user_body.order_status)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 


async def update_orders(user_body : OrdersRequest,db_pool) -> Dict[str,str] : 
    query = f"""
    update orders set
    """
    count = 0
    if user_body.order_status is not None :
        query += f""" order_status = '{user_body.order_status}' """
        count += 1
    if user_body.date_of_delivery is not None :
        if count == 0 : query +=  f""" date_of_delivery = '{user_body.date_of_delivery}'"""
        else : query += f""" ,date_of_delivery = '{user_body.date_of_delivery}'""" 
   
    
    query += f""" where product_id = '{user_body.product_id}' and order_id = '{user_body.order_id}'"""

    print('query',query)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 
    

async def remove_orders(user_body : OrdersRequest,db_pool) -> Dict[str,str] : 
    query = f"""
    delete orders where product_id = {user_body.product_id} and order_id = {user_body.order_id}
    """

    print('query',query)

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                
        return {'error' : None,'data': user_body}
    except Exception as e:
        return {'error' : str(e),'data': None} 


async def get_orders(user_body : OrdersRequest,db_pool) -> Dict[str,str] : 
    query = None

    if user_body.market_id is None and user_body.user_id is None :
        query = """
        SELECT order_id,user_id,
            customer_name,
            product_name,
            product_image_url,
            product_price,
            quantity,
            product_id,
            market_id,
            billing_address,
            date_of_delivery,
            order_status
        FROM orders
        """
    elif user_body.user_id is not None  :
       query ="""
    SELECT order_id, user_id,
           customer_name,
           product_name,
           product_image_url,
           product_price,
           quantity,
           product_id,
           market_id,
           billing_address,
           date_of_delivery,
           order_status
    FROM orders
    WHERE user_id = %s
"""
    elif user_body.market_id is not None  :
       query ="""
    SELECT order_id, user_id,
           customer_name,
           product_name,
           product_image_url,
           product_price,
           quantity,
           product_id,
           market_id,
           billing_address,
           date_of_delivery,
           order_status
    FROM orders
    WHERE market_id = %s
"""

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                if user_body.market_id is not None :
                    await cursor.execute(query, (user_body.market_id,))
                    row = await cursor.fetchall()
                elif user_body.user_id is not None :
                    await cursor.execute(query, (user_body.user_id,))
                    row = await cursor.fetchall()
                else :
                    await cursor.execute(query)
                    row = await cursor.fetchall()
    
        print('row',row)
                
        return {'error' : None,'data': row}
    except Exception as e:
        print('e',e)
        return {'error' : str(e),'data': None}  
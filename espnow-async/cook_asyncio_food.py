import random
import uasyncio as asyncio
import time

async def cook_order(dish_name, duration):
    print(f"Start cooking food : {dish_name}")
    await asyncio.sleep(duration)
    print(f"Finished cooking dish : {dish_name}")

async def serve_food():
    start_time = time.ticks_ms()
    print("Waiting for order...")

    orders = [
        {"name": "Pasta", "time": 2},
        {"name": "Pizza", "time": 4},
        {"name": "Steak", "time": 3},
    ]
    order_tasks = [cook_order(order['name'], order['time']) for order in orders]
    
    await asyncio.gather(*order_tasks)

    print("Finished cooking order. Serving food...")
    
    end_time = time.ticks_ms()
    print(f"Elapsed Time {(end_time - start_time) / 1000} second(s)")

asyncio.run(serve_food())


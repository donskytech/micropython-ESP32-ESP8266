import random
import time

def cook_order(dish_name, duration):
    print(f"Start cooking food : {dish_name}")
    time.sleep(duration)
    print(f"Finished cooking dish : {dish_name}")

def serve_food():
    start_time = time.ticks_ms()
    print("Waiting for order...")

    orders = [
        {"name": "Pasta", "time": 2},
        {"name": "Pizza", "time": 4},
        {"name": "Steak", "time": 3},
    ]

    for order in orders:
        cook_order(order['name'], order['time'])

    print("Finished cooking order. Serving food...")
    
    end_time = time.ticks_ms()
    print(f"Elapsed Time {(end_time - start_time) / 1000} second(s)")

serve_food()



import asyncio

sample_global = 0

async_event = asyncio.Event()

async def update_globals():
    global sample_global
    print('Function Started...')

    await async_event.wait()
    print('Sleep...Before Updating...')

    await asyncio.sleep(1)
    print('Updating...')

    sample_global += 1
    print('Done Updating...')

async def main():

#     tasks = [asyncio.create_task(update_globals()) for _ in range(5)]
    tasks = [update_globals() for _ in range(5)]

    asyncio.gather(*tasks)

    await asyncio.sleep(2)  # Simulating some time before allowing updates
    async_event.set()

    await asyncio.sleep(2)
    print(f"Final value of sample_global: {sample_global}")
    

if __name__ == "__main__":
    asyncio.run(main())


# from random import random
# import asyncio
#  
# # task coroutine
# async def task(event, number):
#     # wait for the event to be set
#     await event.wait()
#     # generate a random value between 0 and 1
#     value = random()
#     # block for a moment
#     await asyncio.sleep(value)
#     # report a message
#     print(f'Task {number} got {value}')
#  
# # main coroutine
# async def main():
#     # create a shared event object
#     event = asyncio.Event()
#     # create and run the tasks
#     tasks = [asyncio.create_task(task(event, i)) for i in range(5)]
#     # allow the tasks to start
#     print('Main blocking...')
#     await asyncio.sleep(0)
#     # start processing in all tasks
#     print('Main setting the event')
#     event.set()
#     # await for all tasks  to terminate
#     await asyncio.wait(tasks)
#  
# # run the asyncio program
# asyncio.run(main())
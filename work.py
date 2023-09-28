import asyncio
import time

import cachetools
from cachetools import TTLCache
from asyncache import cached


class MyClass:
    @cached(cache=TTLCache(ttl=60*5, maxsize=10_000))
    def my_sync_func(self, arg: int):
        print("Called my_sync_func")
        # await asyncio.sleep(arg)
        time.sleep(arg)
        print("Awakening!")
        print("-----------------------------")
        return {"response": {"data": arg}}


def run():
    counter = 0
    value = 0
    while True:
        my_obj = MyClass()
        response = my_obj.my_sync_func(value)
        print(f"Response 1 is received: {response}")
        time.sleep(1)
        counter += 1


run()


def check_cache():
    cache = cachetools.TTLCache(ttl=60 * 5, maxsize=3)

    for i in range(5):
        key = i
        if item := cache.get(key):
            print(item)

        item = key
        cache[key] = item
        print(item)


#check_cache()

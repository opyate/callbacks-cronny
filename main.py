from lib.config import DevConfig
from lib.model.callback import Callback
from lib.handler import async_handle, handle
from lib.collect import read_callbacks_from_db
import asyncio
import multiprocessing
from typing import List
import datetime
import requests
from concurrent.futures import ThreadPoolExecutor


# TODO live check
config = DevConfig


def handle_all(callbacks: List[Callback]):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # async handler will put their results here
    coroutine_list = []

    if callbacks:
        [coroutine_list.append(async_handle(callback)) for callback in callbacks]

        data = loop.run_until_complete(asyncio.wait(coroutine_list))[0]
        loop.close()
        print([d.result() for d in data if d.result() is not None])
    else:
        print('no callbacks to process')

    # task = asyncio.create_task(handle(callback))


cpu_count = multiprocessing.cpu_count()
print('cpu count %i' % cpu_count)


async def handle_all2(callbacks: List[Callback]):
    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    handle,
                    *(session, callback) # Allows us to pass in multiple arguments to `fetch`
                )
                for callback in callbacks
            ]
            for response in await asyncio.gather(*tasks):
                print(response)


if __name__ == '__main__':

    one_min_from_now = datetime.datetime.now() + datetime.timedelta(minutes=1)
    ts = int(one_min_from_now.strftime("%s"))

    callback_list = read_callbacks_from_db(config, ts)

    # single core (option 1)
    # handle_all(callback_list)

    # option 2
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(handle_all2(callback_list))
    loop.run_until_complete(future)



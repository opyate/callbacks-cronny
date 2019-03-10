from lib.model.callback import Callback
import asyncio
from typing import List
from aiohttp import ClientSession, TCPConnector, ClientTimeout


timeout = ClientTimeout(total=5, connect=5)


async def fetch(callback: Callback, session):
    # print('--> callback.id %s' % callback.id)
    async with session.request(callback.http_method, callback.url) as response:
        print('callbacks.id=[%s] %s %s -> %i' % (callback.id, callback.http_method, callback.url, response.status))
        return callback.id, response.status


async def bound_fetch(sem, callback, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(callback, session)


async def run(callbacks: List[Callback]):
    tasks = []
    # create instance of Semaphore
    # TODO make this a function of "max open files"?
    max = 1000
    sem = asyncio.Semaphore(max)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession(connector=TCPConnector(ssl=False), timeout=timeout) as session:
        for callback in callbacks:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, callback, session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def handle(callbacks):

    # from https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(callbacks))
    loop.run_until_complete(future)

    results = future.result()
    return results


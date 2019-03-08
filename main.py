from lib.config import DevConfig
from lib.model.callback import Callback
from lib.handler import handle
from lib.collect import read_callbacks_from_db
import asyncio
import multiprocessing
from typing import List
import datetime


# TODO live check
config = DevConfig
if True:
    config = DevConfig


def handle_all(callbacks: List[Callback]):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # async handler will put their results here
    coroutine_list = []

    if callbacks:
        [coroutine_list.append(handle(callback)) for callback in callbacks]

        data = loop.run_until_complete(asyncio.wait(coroutine_list))[0]
        loop.close()
        print([d.result() for d in data if d.result() is not None])
    else:
        print('no callbacks to process')

    # task = asyncio.create_task(handle(callback))


cpu_count = multiprocessing.cpu_count()
print('cpu count %i' % cpu_count)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

# def main():
#     loop = asyncio.get_event_loop()
#     future = asyncio.ensure_future(get_data_asynchronous())
#     loop.run_until_complete(future)

if __name__ == '__main__':

    one_min_from_now = datetime.datetime.now() + datetime.timedelta(minutes=1)
    ts = int(one_min_from_now.strftime("%s"))

    callback_list = read_callbacks_from_db(config, ts)

    # single core
    handle_all(callback_list)

    # the above code is good enough for now, since it will start a new task if an existing task is waiting

    # below code is a bit silly - I'd rather have cpu_count number of processes take work off
    # a queue once they're done with their existing work.
    # from https://stackoverflow.com/questions/53268438/python-asyncio-within-multiprocessing-one-event-loop-per-process

    # multi core
    # callbacks_chunked = chunks(callback_list, cpu_count)
    # with multiprocessing.Pool(cpu_count) as pool:
    #     data = [j for i in pool.map(handle_all, callbacks_chunked) for j in i]
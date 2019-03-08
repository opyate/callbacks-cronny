from lib.config import DevConfig
from lib.read import read_callbacks
from lib.postprocess import update_callbacks
from lib.handler import handle
import multiprocessing
import datetime


# TODO live check
config = DevConfig


cpu_count = multiprocessing.cpu_count()
print('cpu count %i' % cpu_count)


if __name__ == '__main__':

    one_min_from_now = datetime.datetime.now() + datetime.timedelta(minutes=1)
    ts = int(one_min_from_now.strftime("%s"))

    callback_list = read_callbacks(config, ts)

    # post-process the results
    results = handle(callback_list)

    update_callbacks(config, results)

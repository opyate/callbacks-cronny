from lib.config import DevConfig, ProdConfig
from lib.read import read_callbacks
from lib.postprocess import update_callbacks
from lib.handler import handle
import datetime


import os
config = DevConfig
if 'DO_PROD' in os.environ:
    config = ProdConfig

if __name__ == '__main__':

    one_min_from_now = datetime.datetime.now() + datetime.timedelta(minutes=1)
    # unix time in seconds
    ts = int(one_min_from_now.strftime("%s"))

    callback_list = read_callbacks(config, ts)

    # post-process the results
    results = handle(callback_list)

    update_callbacks(config, results)
    print('done')

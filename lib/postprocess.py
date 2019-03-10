import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from lib.model.callback import Callback
from typing import List
import functools


def update_callbacks(config, results) -> List[Callback]:

    def f(acc, it):
        callback_id = it[0]
        status_code = it[1]
        if status_code >= 400:
            acc['error'].append(callback_id)
        else:
            acc['success'].append(callback_id)
        return acc

    grouped = functools.reduce(f, results, {'success': [], 'error': []})

    update_with_status(config, grouped['success'], 'success')
    update_with_status(config, grouped['error'], 'error')



def update_with_status(config, ids, status):
    url = config.DATABASE_URL
    print(status, ids)
    if ids:
        idsSql = ','.join([str(it) for it in ids])
        with psycopg2.connect(url) as cnn:
            cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with cnn.cursor() as cur:
                cur.execute(
                    sql.SQL("update callbacks set status = %s where id in (" + idsSql + ")").format(),
                    [status]
                )

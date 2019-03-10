import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED
from lib.model.callback import Callback
from typing import List


def read_callbacks(config, ts) -> List[Callback]:
    callbacks = []
    url = config.DATABASE_URL
    with psycopg2.connect(url) as cnn:
        cnn.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
        with cnn.cursor() as cur:
            cur.execute(
                sql.SQL("select * from callbacks where status = 'new' and ts <= %s").format(),
                [ts]
            )

            row = cur.fetchone()
            while row:
                callbacks.append(Callback(row))
                row = cur.fetchone()
    print('db found %i callbacks' % len(callbacks))
    return callbacks

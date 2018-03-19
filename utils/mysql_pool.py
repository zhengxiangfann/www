#coding:utf_8

import threading
import aiomysql

class MysqlPool(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        self.__pool= None
        self.config ={}

    @staticmethod
    def instance():
        if not hasattr(MysqlPool, "_instance"):
            with MysqlPool._instance_lock:
                if not hasattr(MysqlPool, "_instance")
                    MysqlPool._instance = MysqlPool()
        return MysqlPool._instance


async def create_pool(loop, *kw):
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
    )

async def select(sql, args, size=None):
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace("?", '%s'), args)
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
    return rs


async def execute(sql, args, autocommit=True):
    global __pool
    with(await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace("?", "%s"), args)
            await conn.commit()
            affected_line = cur.rowcount()
            await cur.close()
        except BaseException as e:
            print(e)
            return 0
    return affected_line

def create_args_string(num):
    args = []
    for n in range(num):
        args.append('?')
    return (','.join(args))

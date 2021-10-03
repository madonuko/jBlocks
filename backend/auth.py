from os.path import dirname, join

import aiosqlite

root = join(dirname(__file__), "..")


class DBError(Exception):
    """I guess sth went wrong in the db hdl."""


class AuthDB:
    path: str = join(root, "db/auth.db")
    conn: aiosqlite.Connection

    async def _connect(self):
        self.conn = await aiosqlite.connect(self.path)
        await self._sync()

    def __init__(self):
        return self._connect()

    async def add_record(self, table: str, **kws):
        len_d = len(kws)
        S = f"INSERT INTO {table} (" + ", ".join(kws.keys())
        S += f') VALUES ({"?, "*len_d})'
        await self.conn.execute(S, kws.values())
        await self.conn.commit()

    async def get_record(self, table: str, **kws):
        flat = []
        for k, v in kws.items():
            flat.append(k)
            flat.append(v)
        async with self.conn.execute(
            f"SELECT * FROM {table} WHERE "
            + " AND ".join("?=?" for _ in range(len(kws))),
            flat,
        ) as cur:
            return cur

from asyncpg.exceptions import UndefinedTableError, DuplicateTableError
from asyncpg.pool import Pool

import os


class Database:
    """Class to handle database operations"""

    def __init__(self):
        self.query = """CREATE TABLE muted_members(
	                        id VARCHAR(20) PRIMARY KEY
                        )"""

    async def add_muted_role(self, id: str, pool: Pool) -> bool | None:
        muted_members = await self.get_all_muted_role(pool)
        if muted_members is None:
            return

        try:
            if id not in muted_members:
                async with pool.acquire() as connection:
                    async with connection.transaction():
                        # await connection.execute("INSERT INTO MICRO VALUES ('HEY WORLD')")
                        await connection.execute(
                            "INSERT INTO muted_members VALUES ($1)", id
                        )
                return True

            return False
        except UndefinedTableError:
            return

    async def get_all_muted_role(self, pool: Pool) -> list | None:
        val = []
        try:
            async with pool.acquire() as connection:
                async with connection.transaction():
                    # await connection.execute("INSERT INTO MICRO VALUES ('HEY WORLD')")
                    async for record in connection.cursor(
                        "SELECT * FROM muted_members"
                    ):
                        val.append(record["id"])
        except UndefinedTableError:
            return
        return val

    async def remove_muted_role(self, id: str, pool: Pool) -> bool | None:
        muted_members = await self.get_all_muted_role(pool)
        if muted_members is None:
            return
        if id not in muted_members:
            return False
        try:
            async with pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(
                        "DELETE FROM muted_members WHERE id=($1)", id
                    )

            return True

        except UndefinedTableError:
            return
        # logger.info("Muted member removed from database")

    async def create_table(self, pool: Pool) -> bool:
        try:
            async with pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(self.query)
            return True
        except DuplicateTableError:
            return False
        # logger.info("muted_member table has been recreated in the database")

    @classmethod
    def get_dsn(cls) -> str:
        DBUSER = os.getenv("DBUSER")
        DBPASS = os.getenv("DBPASS")
        DBHOST = os.getenv("DBHOST")
        DBPORT = os.getenv("DBPORT")
        DBDATABASE = os.getenv("DBDATABASE")

        PG_URL = f"postgres://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBDATABASE}"
        return PG_URL

from sqlmodel import SQLModel

from core.database import engine


async def create_tables() -> None:
    import models.__all_models
    print('creating database tables')

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    
    print('tables created successfully')


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())

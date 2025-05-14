from sqlalchemy import delete
from db.session import async_session
from models import UserChoices
  



async def clear_user_choices(user_id: int):
    async with async_session() as session:
        stmt = delete(UserChoices).where(UserChoices.user_id == user_id)
        await session.execute(stmt)
        await session.commit()

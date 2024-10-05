from app.database.models import User


async def create_user(tg_id: int, username: str = None, ):
    await User.create(username=username, tg_id=tg_id)
    return

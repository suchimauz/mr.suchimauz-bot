from sqlalchemy import sql, Column

from utils.db.database import db


class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50))
    last_activity = Column(db.DateTime, nullable=True)


# Функция для получения юзера по айди
async def get_user(user_id) -> User:
    user = await User.query.where(User.id == user_id).gino.first()
    return user

# Функция для создания или обновления пользователя
async def add_user(**kwargs):
    user_id = kwargs.get('id')
    user = await get_user(user_id)

    if user is None:
        new_user = await User(**kwargs).create()
        return new_user

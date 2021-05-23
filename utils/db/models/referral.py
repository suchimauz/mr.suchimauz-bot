from sqlalchemy import sql, Column

from utils.db.database import db
from utils.db.models.user import User


class Referral(db.Model):
    __tablename__ = "referrals"
    query: sql.Select

    user_id = Column(None, db.ForeignKey("users.id"), primary_key=True)
    referrer_id = Column(None, db.ForeignKey("users.id"))


async def get_referrer_user_by_user_id(user_id) -> User:
    row = await Referral.query.where(Referral.user_id == user_id).gino.first()

    return await User.query.where(User.id == row.referrer_id).gino.first()


async def add_new_referrer_for_user(user_id, referrer_id):
    return await Referral(user_id=user_id, referrer_id=referrer_id).create()

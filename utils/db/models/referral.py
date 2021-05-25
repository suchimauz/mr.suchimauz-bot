from sqlalchemy import sql, Column

from utils.db.database import db
from utils.db.models.user import User


class Referral(db.Model):
    __tablename__ = "referrals"
    query: sql.Select

    user_id = Column(None, db.ForeignKey("users.id"), primary_key=True)
    referrer_id = Column(None, db.ForeignKey("users.id"))


async def get_referrer_user_by_user_id(user_id) -> User:
    row = await Referral.query.where(Referral.user_id == int(user_id)).gino.first()

    if row:
        return await User.query.where(User.id == row.referrer_id).gino.first()
    else:
        return None


async def add_new_referrer_for_user(user_id, referrer_id):
    return await Referral(user_id=user_id, referrer_id=referrer_id).create()


async def get_referrals_count_by_referrer_id(user_id):
    query = db.text(
        f"SELECT count(r.*) "
        f"FROM users u "
        f"JOIN referrals r "
        f"ON r.referrer_id = u.id "
        f"WHERE u.id = {int(user_id)}"
    )
    result = await db.first(query)

    if result[0]:
        return result[0]
    else:
        return 0


async def get_referrals_cost_by_referrer_id(user_id):
    query = db.text(
        f"SELECT sum(t.cost) "
        f"FROM referrals r "
        f"JOIN users u "
        f"ON u.id = r.user_id "
        f"JOIN transactions t "
        f"ON t.user_id = u.id "
        f"WHERE r.referrer_id = {int(user_id)}"
    )
    result = await db.first(query)

    if result[0]:
        return result[0]
    else:
        return 0

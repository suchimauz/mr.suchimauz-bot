from typing import List

from sqlalchemy import sql, Column
from sqlalchemy.dialects.postgresql import JSONB

from utils.db.database import db


class Mail(db.Model):
    __tablename__ = "mails"
    query: sql.Select

    email = Column(db.String, primary_key=True)
    password = Column(db.String)
    reserved_email = Column(db.String, nullable=True)
    imap = Column(db.String)
    uses = Column(JSONB, default=[])


async def get_mail_by_email(email) -> Mail:
    return await Mail.query.where(Mail.email == email).gino.first()

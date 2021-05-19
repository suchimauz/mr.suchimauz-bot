from typing import List

from sqlalchemy import sql, Column
from sqlalchemy.dialects.postgresql import JSONB

from utils.db.database import db


class Mail(db.Model):
    __tablename__ = "mails"
    query: sql.Select

    mail = Column(db.String, primary_key=True)
    password = Column(db.String)
    reserve_mail = Column(db.String, nullable=True)
    uses = Column(JSONB, default=[])



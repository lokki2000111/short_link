from uuid import uuid4

import sqlalchemy as sa

from engine import Base


class URL(Base):
    __tablename__ = "urls"

    id = sa.Column(sa.Integer, primary_key=True)
    key = sa.Column(sa.String, unique=True)
    target_url = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean, default=True)
    clicks = sa.Column(sa.Integer, default=0)

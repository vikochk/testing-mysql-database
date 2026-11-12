from datetime import datetime
from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class SessionModel(BaseModel):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    build_number: Mapped[int] = mapped_column(BigInteger, nullable=False)

    test: Mapped['Test'] = relationship('Test', back_populates='session')
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class Log(BaseModel):
    __tablename__ = 'log'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    content: Mapped[str | None] = mapped_column(LONGTEXT, nullable=True)
    is_exception: Mapped[int | None] = mapped_column(TINYINT(1), nullable=True)
    test_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('test.id'), nullable=False)

    test: Mapped['Test'] = relationship('Test', back_populates='logs')
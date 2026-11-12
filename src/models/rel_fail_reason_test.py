from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class RelFailReasonTest(BaseModel):
    __tablename__ = 'rel_fail_reason_test'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    fail_reason_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    test_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('test.id'), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    test: Mapped['Test'] = relationship('Test', back_populates='fail_reasons')
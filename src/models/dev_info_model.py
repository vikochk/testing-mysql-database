from sqlalchemy import BigInteger, Double, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class DevInfo(BaseModel):
    __tablename__ = 'dev_info'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    dev_time: Mapped[float | None] = mapped_column(Double, nullable=True)
    test_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('test.id'), nullable=False)

    test: Mapped['Test'] = relationship('Test', back_populates='dev_infos')
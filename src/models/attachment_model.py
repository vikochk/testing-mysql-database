from sqlalchemy import BigInteger, ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class Attachment(BaseModel):
    __tablename__ = 'attachment'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    content: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    test_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('test.id'), nullable=False)

    test: Mapped['Test'] = relationship('Test', back_populates='attachments')
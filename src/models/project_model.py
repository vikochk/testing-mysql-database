from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class Project(BaseModel):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    test: Mapped['Test'] = relationship('Test', back_populates='project')
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class Test(BaseModel):
    __test__ = False
    __tablename__ = 'test'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    status_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('status.id'), nullable=True)
    method_name: Mapped[str] = mapped_column(String(10000), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey('session.id'), nullable=False)
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    env: Mapped[str] = mapped_column(String(255), nullable=False)
    browser: Mapped[str | None] = mapped_column(String(255), nullable=True, default='')
    author_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('author.id'), nullable=True)

    author: Mapped['Author | None'] = relationship('Author', back_populates='test')
    project: Mapped['Project'] = relationship('Project', back_populates='test')
    session: Mapped['SessionModel'] = relationship('SessionModel', back_populates='test')
    status: Mapped['Status | None'] = relationship('Status', back_populates='test')

    attachments: Mapped[list['Attachment']] = relationship('Attachment', back_populates='test', cascade='all, delete-orphan')
    dev_infos: Mapped[list['DevInfo']] = relationship('DevInfo', back_populates='test', cascade='all, delete-orphan')
    logs: Mapped[list['Log']] = relationship('Log', back_populates='test', cascade='all, delete-orphan')
    fail_reasons: Mapped[list['RelFailReasonTest']] = relationship('RelFailReasonTest', back_populates='test', cascade='all, delete-orphan')
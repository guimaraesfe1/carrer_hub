from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, Session, mapped_column

from .base import Base


class Inscription(Base):
    __tablename__ = 'inscriptions'

    job_id: Mapped[int] = mapped_column(
        ForeignKey('jobs.id'), primary_key=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id'), primary_key=True
    )
    why: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), init=False
    )

    @classmethod
    def create_inscription(
        cls,
        job_id: int,
        student_id: int,
        data_inscription: dict,
        session: Session,
    ):
        inscription = session.get(cls, (job_id, student_id))

        if inscription:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Inscrição ja existe',
            )

        new_inscription = cls(
            student_id=student_id,
            job_id=job_id,
            **data_inscription,
        )

        session.add(new_inscription)
        session.commit()

    @classmethod
    def update_inscription(
        cls,
        job_id: int,
        student_id: int,
        inscription_update: dict,
        session: Session,
    ):
        getInscription = session.get(cls, (job_id, student_id))

        if not getInscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Inscrição não encontrada',
            )

        for key, value in inscription_update:
            if value is None:
                continue

            setattr(getInscription, key, value)

        session.commit()

    @classmethod
    def delete_inscription(cls, job_id, student_id, session: Session):
        getInscription = session.get(cls, (job_id, student_id))

        if not getInscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Inscrição não encontrada!',
            )

        session.delete(getInscription)
        session.commit()

    @classmethod
    def get_inscription(cls, job_id, student_id, session: Session):
        getInscription = session.get(cls, (job_id, student_id))

        if not getInscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Inscrição não encontrada!',
            )

        return getInscription

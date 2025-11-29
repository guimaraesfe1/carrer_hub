from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, Session, mapped_column

from ..schemas.job import CreateJobSchema, UpdateJobSchema
from .base import Base
from .company import Company


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(nullable=False)
    started_in: Mapped[date] = mapped_column(
        nullable=False, server_default=func.current_date(), init=False
    )
    ended_in: Mapped[date | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))

    @classmethod
    def create_job(
        cls, company_id: int, job_data: CreateJobSchema, session: Session
    ):
        getCompany = session.get(Company, company_id)

        if not getCompany:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Vaga não criada! Empresa não existe',
            )

        new_job = Job(
            title=job_data.title,
            ended_in=job_data.ended_in,
            description=job_data.description,
            company_id=company_id,
        )

        session.add(new_job)
        session.commit()

    @classmethod
    def update_job(
        cls,
        job_id: int,
        job_data_update: UpdateJobSchema,
        company_id: int,
        session: Session,
    ):
        try:
            data_update = job_data_update.model_dump()

            get_job = session.get(cls, job_id)
            if not get_job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Vaga não encontrada!',
                )

            if get_job.company_id != company_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Não tem permissão para atualizar essa vaga!',
                )

            for key, value in data_update.items():
                if value is None:
                    continue

                setattr(get_job, key, value)

            session.commit()
        except Exception:
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro interno do servidor',
            ) from None

    @classmethod
    def delete_job(cls, job_id: int, company_id: int, session: Session):
        get_job = session.get(cls, job_id)

        if not get_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Vaga não encontrada',
            )

        if get_job.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Não tem permissão para acessar esse recurso!',
            )

        session.delete(get_job)
        session.commit()

    @classmethod
    def get_job(cls, job_id: int, session: Session):
        get_job = session.get(cls, job_id)

        if not get_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Vaga não encontrada!',
            )

        return get_job

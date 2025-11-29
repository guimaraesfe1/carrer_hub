from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import ForeignKey, String, delete
from sqlalchemy.orm import Mapped, Session, mapped_column

from ..schemas.auth import AccountSignUpSchema
from .account import Account
from .base import Base


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(
        ForeignKey('accounts.id'), primary_key=True
    )
    first_name: Mapped[str] = mapped_column(
        String(30), nullable=False, default=None
    )
    last_name: Mapped[str] = mapped_column(
        String(30), nullable=False, default=None
    )
    birth_date: Mapped[date] = mapped_column(nullable=True, default=None)
    course: Mapped[str] = mapped_column(nullable=False, default=None)

    @classmethod
    def create_student(
        cls, account_data: AccountSignUpSchema, session: Session
    ):
        new_account_id = Account._create_account(account_data, session)

        new_student = cls(id=new_account_id)

        session.add(new_student)
        session.commit()

    @classmethod
    def update_student(
        cls, student_id: int, data_update: dict, session: Session
    ):
        try:
            get_student = session.get(cls, student_id)

            if not get_student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Estudante não encontrado',
                )

            for key, value in data_update.items():
                if value is None:
                    continue

                setattr(get_student, key, value)

            session.commit()
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro interno do servidor',
            ) from None

    @classmethod
    def delete_student(cls, student_id: int, session: Session):
        try:
            session.execute(delete(cls).where(cls.id == student_id))
            session.execute(delete(Account).where(Account.id == student_id))

            session.commit()
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro interno do servidor',
            ) from None

from fastapi import HTTPException, status
from sqlalchemy import ForeignKey, delete
from sqlalchemy.orm import Mapped, Session, mapped_column

from ..models.account import Account
from ..schemas.auth import AccountSignUpSchema
from .base import Base


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(
        ForeignKey('accounts.id'), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, default=None)
    legal_name: Mapped[Optional[str]] = mapped_column(String(150))
    cnpj: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    @classmethod
    def create_company(
        cls, account_data: AccountSignUpSchema, session: Session
    ):
        try:
            account_id = Account._create_account(account_data, session)

            new_company = cls(id=account_id)

            session.add(new_company)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def update_company(
        cls, company_id: int, data_update: dict, session: Session
    ):
        try:
            get_company = session.get(cls, company_id)

            if not get_company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Empresa não encontrada',
                )

            for key, value in data_update.items():
                if value is None:
                    continue

                setattr(get_company, key, value)

            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def delete_student(cls, company_id: int, session: Session):
        try:
            session.execute(delete(cls).where(cls.id == company_id))
            session.execute(delete(Account).where(Account.id == company_id))

            session.commit()
        except Exception:
            session.rollback()
            raise

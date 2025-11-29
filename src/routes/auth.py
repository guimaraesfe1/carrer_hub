from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database.session import getSession
from ..models.account import Account
from ..schemas.auth import Token
from ..security.encryption import passwd_hash
from ..utils.tokenization import create_token

router = APIRouter(prefix='/api/auth', tags=['auth'])


@router.post('/v1/sign-in', status_code=status.HTTP_201_CREATED)
def signInAccount(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(getSession)],
):
    getAccount = Account.getAccountByEmail(form_data.username, session)

    if not passwd_hash.verify(form_data.password, getAccount.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais incorretas!',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    payload = {
        'sub': str(getAccount.id),
        'role': getAccount.role,
    }

    token = create_token(payload)

    return Token(access_token=token, token_type='bearer')

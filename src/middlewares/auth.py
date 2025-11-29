from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from ..database.session import getSession
from ..models.account import Account
from ..security.enviroment import env_settings
from ..utils.enums import AccountRole

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/v1/sign-in')

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def validateAccount(
    token: Annotated[str, Depends(oauth_scheme)],
    session: Annotated[Session, Depends(getSession)],
):
    try:
        payload = decode(
            jwt=token,
            key=env_settings['JWT_SECRET_KEY'],
            algorithms=env_settings['ALGORITHM'],
        )

        if payload['sub'] is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception from None

    account_data = Account.getACcountById(int(payload['sub']), session)

    if not account_data:
        raise credentials_exception

    return payload


def validateAccountStudent(payload: Annotated[dict, Depends(validateAccount)]):
    if payload['role'] != AccountRole.STUDENT:
        raise credentials_exception

    return int(payload['sub'])


def validateAccountCompany(payload: Annotated[dict, Depends(validateAccount)]):
    if payload['role'] != AccountRole.COMPANY:
        raise credentials_exception

    return int(payload['sub'])


from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.session import getSession
from ..models.inscription import Inscription  # Ajuste o nome se for diferente
from ..schemas.inscription import CreateInscriptionSchema  # Ajuste o nome se for diferente

# Mantendo o padrão de prefixo '/api/...' visto nos outros arquivos
router = APIRouter(prefix='/api/inscription', tags=['inscription'])


@router.post('/v1/{jobopening_id}/{student_id}', status_code=status.HTTP_201_CREATED)
def createInscription(
    jobopening_id: int,
    student_id: int,
    inscription_data: CreateInscriptionSchema,
    session: Annotated[Session, Depends(getSession)],
):
    Inscription.create_inscription(
        job_id=jobopening_id,
        student_id=student_id,
        data=inscription_data,
        session=session,
    )

    return {'message': 'Inscrição realizada com sucesso!'}
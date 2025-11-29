from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.session import getSession
from ..middlewares.auth import validateAccountStudent
from ..models.inscription import Inscription
from ..schemas.inscription import (
    InscriptionCreateSchema,
    InscriptionUpdateSchema,
)

router = APIRouter(prefix='/api/inscription', tags=['inscription'])


@router.get('/v1/{job_id}/{student_id}')
def getInscription(
    student_id: int,
    job_id: int,
    session: Annotated[Session, Depends(getSession)],
):
    getInscription = Inscription.get_inscription(
        job_id=job_id, session=session, student_id=student_id
    )

    return getInscription


@router.post('/v1/{job_id}')
def createInscription(
    current_student_id: Annotated[int, Depends(validateAccountStudent)],
    job_id: int,
    inscription_data: InscriptionCreateSchema,
    session: Annotated[Session, Depends(getSession)],
):
    Inscription.create_inscription(
        job_id, current_student_id, inscription_data.model_dump(), session
    )

    return {'message': 'Inscrição criada com sucesso'}


@router.delete('/v1/{job_id}')
def deleteInscription(
    current_student_id: Annotated[int, Depends(validateAccountStudent)],
    job_id: int,
    session: Annotated[Session, Depends(getSession)],
):
    Inscription.delete_inscription(job_id, current_student_id, session)

    return {'message': 'Inscrição deletada!'}


@router.put('/v1/{job_id}')
def updateInscription(
    current_student_id: Annotated[int, Depends(validateAccountStudent)],
    job_id: int,
    inscription_data: InscriptionUpdateSchema,
    session: Annotated[Session, Depends(getSession)],
):
    Inscription.update_inscription(
        job_id, current_student_id, inscription_data.model_dump(), session
    )

    return {'message': 'Inscrição atualizada com sucesso!'}

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.session import getSession
from ..middlewares.auth import validateAccountCompany
from ..models.job import Job
from ..schemas.job import CreateJobSchema, UpdateJobSchema

router = APIRouter(prefix='/api/job', tags=['job'])


@router.post('/v1/', status_code=status.HTTP_201_CREATED)
def createJob(
    current_company_id: Annotated[int, Depends(validateAccountCompany)],
    job_data: CreateJobSchema,
    session: Annotated[Session, Depends(getSession)],
):
    Job.create_job(current_company_id, job_data, session)

    return {'message': 'Vaga criada com sucesso!'}


@router.delete('/v1')
def deleteJob(
    job_id: int,
    current_company_id: Annotated[int, Depends(validateAccountCompany)],
    session: Annotated[Session, Depends(getSession)],
):
    Job.delete_job(
        job_id=job_id, company_id=current_company_id, session=session
    )

    return {'message': 'Vaga deletada com sucesso'}


@router.put('/v1/{job_id}', status_code=status.HTTP_200_OK)
def updateJob(
    job_id: int,
    job_data: UpdateJobSchema,
    current_company_id: Annotated[int, Depends(validateAccountCompany)],
    session: Annotated[Session, Depends(getSession)],
):
    Job.update_job(
        job_id=job_id,
        job_data_update=job_data,
        company_id=current_company_id,
        session=session,
    )

    return {'message': 'Vaga atualizada com sucesso!'}


@router.get('/v1', status_code=status.HTTP_200_OK)
def getJob(
    job_id: int,
    session: Annotated[Session, Depends(getSession)],
):
    return Job.get_job(job_id=job_id, session=session)

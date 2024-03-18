import logging

from fastapi import APIRouter
from starlette import status

from health.presentation import schema as s

lg = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    response_model=s.HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check():
    lg.info('Running health check')
    return {"message": "I'm healthy!"}

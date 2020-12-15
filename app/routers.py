from fastapi import APIRouter

router = APIRouter(prefix='/v1/statistics')

from . import views  # noqa

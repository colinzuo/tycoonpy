from typing import Any

from fastapi import APIRouter
from hpyhrtbase.model import CommonResult

from tycoonpy.utils import ContextUtil

router = APIRouter(prefix="/user_quality")

@router.get("/get_user_quality_distribution_list")
def get_user_quality_distribution_list(
) -> CommonResult[Any]:
    user_quality_service = ContextUtil.get_user_quality_service()

    distribution_list = user_quality_service.get_user_quality_distribution_list(
    )

    rsp = CommonResult[Any](data=distribution_list)

    return rsp

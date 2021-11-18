from datetime import datetime
from calendar import monthrange
from core.db import get_db
from fastapi import APIRouter
from sqlalchemy.orm import Session
from core.ratelimit import RateLimit
from fastapi import APIRouter, Depends
from core.schemas import View


router = APIRouter(prefix="/fetch")

@router.get("/views/{public_key}", 
            dependencies=[Depends(RateLimit(times=20, seconds=5))],
            status_code=200)
async def views(public_key: str, db: Session=Depends(get_db)) -> dict:

    views = db.query(View).filter_by(public_key=public_key)
    current_month = datetime.utcnow().month
    month_data = [x.viewed_on for x in views if x.viewed_on.month == current_month]
    amount_of_days = monthrange(2021, current_month)[1]
    data = {}
    for i in range(1, amount_of_days + 1):
        if i not in [x.day for x in month_data]:
            data.update({i: 0})
        else:
            for d in month_data:
                if d.day in data.keys():
                    data[d.day] += 1
                else:
                    data.update({d.day: 1})

    return data
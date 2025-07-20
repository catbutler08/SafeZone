from fastapi import APIRouter, Depends, HTTPException, Form
from datetime import datetime, timezone
from ..db.mongo import users, gpses
from .auth import get_current_user

router = APIRouter(prefix="/account", tags=["Account"])

# 계정 삭제
@router.delete("/delete", status_code=204)
def delete_account(current=Depends(get_current_user)):
    users.delete_one({"_id": current["_id"]})
    gpses.delete_many({"username": current["username"]})

# GPS 업로드
@router.post("/gps")
def gps_update(
    lat: float = Form(...),
    lon: float = Form(...),
    current=Depends(get_current_user)
):
    if current["role"] != "Protecter":
        raise HTTPException(403, "권한 없음")
    gpses.insert_one({
        "username": current["username"],
        "lat": lat,
        "lon": lon,
        "createdAt": datetime.now(timezone.utc)
    })
    return {"msg": "업로드 완료"}

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
@router.post("/info/gps")
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


#RSSI 베터리 정보 수신
@router.post("/info/device")
def device_info(RSSI: int = Form(...), Battery: int = Form(...), current = Depends(get_current_user)):
    if(current["role"] == "Protecter"):
        raise HTTPException(400, "정보 수신이 필요하지 않음")
    else:
        users.find_one_and_update({"username": current["name"]},{"RSSI": RSSI,"Battery": Battery})
        user = users.find_one({"usernmae":current["name"]})
        if user.get("RSSI") != RSSI or user.get("Battery") != Battery:
            raise HTTPException(401, "db업데이트 추가 실패")
        else:
            return {"msg": "정보 수신 성공"}
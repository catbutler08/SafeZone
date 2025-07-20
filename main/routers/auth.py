from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from ..schemas.user import UserIn, Token
from ..core import security
from ..db.mongo import users
from ..utils.email import is_valid

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 회원가입 (보호자)
@router.post("/register/protecter", status_code=201)
def register_protecter(
    name: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    telephone: str = Form(...)
):
    # 중복 검사
    for field, value in (("username", username), ("email", email), ("telephone", telephone)):
        if users.find_one({field: value}):
            raise HTTPException(status_code=400, detail=f"이미 존재하는 {field}")
    if not is_valid(email):
        raise HTTPException(status_code=401, detail="올바르지 않은 이메일")

    hashed = security.hash_password(password)
    users.insert_one({
        "name": name,
        "email": email,
        "username": username,
        "password": hashed,
        "role": "Protecter",
        "telephone": telephone
    })
    return {"msg": "회원가입 완료"}

# 로그인
@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({"username": form_data.username})
    if not user or not security.verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="로그인 실패")
    token = security.create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# 현재 사용자
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = security.decode_token(token)
    username = payload.get("sub")
    user = users.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="사용자 없음")
    return user

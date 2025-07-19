from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pymongo import MongoClient


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()

# 세션 쿠키 암호화
SECRET_KEY = "657df88713959387d83a9da5fbda9e872d5739d24065d59adbe463decdb58324"

# MongoDB 연결
client = MongoClient("mongodb+srv://Wsuck:6qvd5ThUkCaZMdRQ@cluster0.kupvcum.mongodb.net/")
db = client["CODEFAIR"]
users = db["user"]

# 보안 관련
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    from datetime import timezone
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#  유저 인증
def authenticate_user(username: str, password: str):
    user = users.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return False
    return {"username": username}


# JWT에서 사용자 추출
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="토큰이 유효하지 않음",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"username": username}
    except JWTError:
        raise credentials_exception


# 회원가입
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자")
    hashed_pw = get_password_hash(password)
    users.insert_one({"username": username, "password": hashed_pw})
    return {"message": "회원가입 완료"}

#  로그인 (JWT 토큰 발급)
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

#  로그인 상태 확인
@app.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pymongo import MongoClient
from pymongo import ASCENDING
from email_validator import validate_email, EmailNotValidError
from datetime import timezone


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()

# 세션 쿠키 암호화
SECRET_KEY = "657df88713959387d83a9da5fbda9e872d5739d24065d59adbe463decdb58324" #서비스 완성시 변경 예정

# MongoDB 연결
client = MongoClient("mongodb+srv://Wsuck:6qvd5ThUkCaZMdRQ@cluster0.kupvcum.mongodb.net/")
db = client["SafeZone"]
users = db["user"]
gpses = db['gps']
gpses.create_index([("createdAt", ASCENDING)], expireAfterSeconds=7776000)

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
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#  유저 인증
async def authenticate_user(username: str, password: str):
    user = await users.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return False
    return {"username": username}


# JWT에서 사용자 추출
def get_current_user(token: str = Depends(oauth2_scheme)):
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

#이메일 유효성 검사
def email_vaild(email:str)->bool:
    try:
        info = validate_email(
            email,
            allow_smtputf8=False,     
            check_deliverability=True 
        )
        print("정상:", info.normalized)  
        return True
    except EmailNotValidError as e:
        print("오류:", str(e))
        return False
    

#여기부터 라우팅

# 회원가입
@app.post("/register/protecter")
async def register(name: str = Form(...),email: str = Form(...),username: str = Form(...), password: str = Form(...),telephone: str = Form(...)):
    if await users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자")
    if await users.find_one({"email":email}):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일")
    if email_vaild(email) == False:
        raise HTTPException(status_code=400, detail="올바르지 않은 이메일")
    if await users.find_one({"telephone":telephone}):
        raise HTTPException(status_code=400, detail="이미 존재하는 전화번호")
    hashed_pw = get_password_hash(password)
    await users.insert_one({"name": name,"email": email,"username": username, "password": hashed_pw,"role":"Protecter","telephone": telephone})
    return {"message": "회원가입 완료"}

# 회원가입 피보호자(만들어야함)
# @app.post("/register/user")
# def register(username: str = Form(...), password: str = Form(...)):
#     if users.find_one({"username": username}):
#         raise HTTPException(status_code=400, detail="이미 존재하는 사용자")
#     hashed_pw = get_password_hash(password)
#     users.insert_one({"username": username, "password": hashed_pw,"role":"Protecter"})
#     return {"message": "회원가입 완료"}  

#로그인 (JWT 토큰 발급)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


#비번 변경, 아이디 찾기 만들어ㅓㅓㅓㅓㅓㅓㅓㅓ


#계정 삭제
@app.delete("/account/delete")
async def delete_account(current: dict = Depends(get_current_user)):
    user = await users.find_one({"username": current["username"]})
    await users.delete_one({"_id": user["_id"]})
    await gpses.delete_many({"username": user["username"]})
    return {"message": "계정 및 관련 데이터가 삭제되었습니다"}


#로그인 상태 확인
@app.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user

#gps넣기 + 베터리, 수신강도 데이터(만들어야함)
@app.post("/gps")
async def gps(lat: float = Form(...),lon: float = Form(...),current_user: dict = Depends(get_current_user)):
    role = await users.find_one({"username":current_user["username"]}).get("role")
    if role != "Protecter":
        gpses.insert_one({"username":role.get("username"),"lat":lat,"lon":lon,"createdAt": datetime.now(timezone.utc)})
        

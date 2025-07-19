from fastapi import FastAPI, Request, Form, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from itsdangerous import URLSafeSerializer

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시에는 정확한 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 쿠키 암호화
SECRET_KEY = "super_secret"
serializer = URLSafeSerializer(SECRET_KEY, salt="session")

# MongoDB 연결
client = MongoClient("mongodb+srv://Wsuck:6qvd5ThUkCaZMdRQ@cluster0.kupvcum.mongodb.net/")
db = client["CODEFAIR"]
users = db["users"]

# 현재 로그인 사용자 확인 함수
def get_current_user(request: Request):
    cookie = request.cookies.get("session")
    if not cookie:
        return None
    try:
        session = serializer.loads(cookie)
        return session.get("username")
    except:
        return None

# 회원가입
@app.post("/register")
async def register(response: Response, username: str = Form(...), password: str = Form(...)):
    if users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    users.insert_one({"username": username, "password": password})
    session = serializer.dumps({"username": username})
    response.set_cookie("session", session, httponly=True, samesite="Lax")
    return {"message": "회원가입 성공", "username": username}

# 로그인
@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    user = users.find_one({"username": username})
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="로그인 실패")
    session = serializer.dumps({"username": username})
    response.set_cookie("session", session, httponly=True, samesite="Lax")
    return {"message": "로그인 성공", "username": username}

# 현재 로그인된 사용자 정보 확인
@app.get("/me")
async def me(request: Request):
    username = get_current_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="로그인 필요")
    return {"username": username}

# 로그아웃
@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "로그아웃 성공"}

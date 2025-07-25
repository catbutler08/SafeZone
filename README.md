# SafeZone (임시 README)
> ⚠️ 이 문서는 임시 버전이며, 기능·설명·예제 등이 향후 확정되면 수정될 예정입니다.

## 프로젝트 개요
**SafeZone은 보호자‑피보호자 위치 안전 서비스를 위한 FastAPI 백엔드입니다. JWT 인증과 MongoDB 기반 GPS 기록 저장 기능을 제공합니다.**

## 주요 기능 (초안)
  * JWT 기반 사용자 인증
  * 역할 기반 계정: Protector(보호자) / (예정) Child(피보호자)
  * MongoDB TTL 인덱스로 90 일 지난 GPS 기록 자동 삭제
  * REST API: 회원가입, 로그인, 프로필 조회, 계정 삭제, GPS 업로드
> TODO: 이메일 인증, 실시간 알림 푸시 기능 추가 예정

## 기술 스택
|영역|사용 기술|
|------|---|
|웹 프레임워크|FastAPI (Python 3.11+)|
|인증·보안|python‑jose, passlib[bcrypt]|
|데이터베이스|MongoDB|
|데이터 모델|Pydantic|

## 폴더 구조 (요약)
    SafeZone-main/
    ├── main/            # 백엔드 코드
    │   ├── core/        # 설정·보안 유틸리티
    │   ├── db/          # MongoDB 클라이언트
    │   ├── routers/     # API 엔드포인트
    │   ├── schemas/     # Pydantic 모델
    │   └── main.py
    └── test/
        └── test.js      # 예시 스크립트

## 환경 변수
`.env` 파일 또는 환경 변수로 다음 값을 설정합니다.

|변수|설명|
|----|---|
|`SECRET_KEY`|JWT 서명에 사용될 비밀 키|
|`MONGO_URI`|MongoDB 접속 문자열|
|`DB_NAME`|사용할 데이터베이스 이름|

## 설치 및 실행
```bash
pip install -r requirements.txt       # 의존성 설치
uvicorn main.main:app --reload --port 8000  # 로컬 서버 실행
```

## 테스트 실행
백엔드 API 테스트는 Node 18 이상에서 다음과 같이 실행합니다.
```bash
node test/test.js
```

##API 요약 (임시)

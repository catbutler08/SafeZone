# SafeZone (임시 README)
> ⚠️ 이 문서는 임시 버전이며, 기능·설명·예제 등이 향후 확정되면 수정될 예정입니다.

## 프로젝트 개요
**SafeZone은 보호자‑피보호자 위치 안전 서비스를 위한 FastAPI 백엔드입니다. JWT 인증과 MongoDB 기반 GPS 기록 저장 기능을 제공합니다.**

## 주요 기능 (초안)
  • JWT 기반 사용자 인증

  • 역할 기반 계정: Protector(보호자) / (예정) Child(피보호자)

  • MongoDB TTL 인덱스로 90 일 지난 GPS 기록 자동 삭제

  • REST API: 회원가입, 로그인, 프로필 조회, 계정 삭제, GPS 업로드

  • OpenAPI(Swagger) 자동 문서화

> TODO: 이메일 인증, 실시간 알림 푸시 기능 추가 예정
>

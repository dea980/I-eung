# I-eung (이응) 프로젝트

## 프로젝트 소개
I-eung은 레시피 관리와 쇼핑 리스트 기능을 제공하는 웹 애플리케이션입니다.

## 기술 스택

### 프론트엔드
- React
- TypeScript
- Tailwind CSS
- Context API (상태 관리)

### 백엔드
- Python
- OAuth 인증
- RESTful API

## 주요 기능

### 1. 사용자 인증
- OAuth 기반 로그인 시스템
- 사용자 프로필 관리

### 2. 레시피 관리
- 레시피 조회 및 상세 보기
- 레시피 카드 형태의 직관적인 UI
- 레시피 상세 정보 제공

### 3. 쇼핑 리스트
- 필요한 재료 관리
- 쇼핑 리스트 생성 및 관리

## 프로젝트 구조

```
프로젝트 루트/
├── frontend/                # 프론트엔드 애플리케이션
│   ├── src/
│   │   ├── api/            # API 클라이언트
│   │   ├── components/     # 재사용 가능한 컴포넌트
│   │   ├── contexts/       # React Context
│   │   ├── pages/         # 페이지 컴포넌트
│   │   └── types/         # TypeScript 타입 정의
│   └── public/            # 정적 파일
│
├── backend/               # 백엔드 서버
│   ├── oauth_config.py   # OAuth 설정
│   └── oauth_routes.py   # OAuth 라우트 처리
│
└── requirements.txt      # Python 의존성 패키지
```

## 설치 및 실행 방법

### 백엔드 설정
```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```

### 프론트엔드 설정
```bash
# frontend 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

## 환경 변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음 환경 변수를 설정하세요:
```
# OAuth 설정
OAUTH_CLIENT_ID=your_client_id
OAUTH_CLIENT_SECRET=your_client_secret

# 기타 설정
API_BASE_URL=http://localhost:your_port
```

## API 문서
자세한 API 명세는 `API설명서.md` 파일을 참조하세요.

## 개발 가이드라인
- 모든 프론트엔드 코드는 TypeScript로 작성
- 컴포넌트는 재사용성을 고려하여 설계
- 백엔드 API는 RESTful 원칙을 준수

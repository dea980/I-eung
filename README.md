# 게시글 추천 시스템 API

사용자 선호도 기반의 게시글 추천 기능이 포함된 Django REST API 시스템입니다.

## 주요 기능

- 게시글, 댓글, 카테고리, 태그에 대한 전체 CRUD 작업
- 사용자 인증 및 권한 관리
- 사용자 선호도 기반 게시글 추천 시스템
- 좋아요/싫어요 기능
- 평점 시스템
- 검색 및 필터링 기능
- 페이지네이션 지원

## API 엔드포인트

### 게시글
- `GET /api/articles/` - 전체 게시글 목록
- `POST /api/articles/` - 새 게시글 작성
- `GET /api/articles/{id}/` - 특정 게시글 조회
- `PUT /api/articles/{id}/` - 게시글 수정
- `DELETE /api/articles/{id}/` - 게시글 삭제
- `POST /api/articles/{id}/like/` - 게시글 좋아요
- `POST /api/articles/{id}/dislike/` - 게시글 싫어요
- `POST /api/articles/{id}/rate/` - 게시글 평가
- `GET /api/articles/recommended/` - 개인화된 게시글 추천
- `GET /api/articles/top_rated/` - 최고 평점 게시글

### 카테고리
- `GET /api/categories/` - 전체 카테고리 목록
- `POST /api/categories/` - 새 카테고리 생성
- `GET /api/categories/{id}/` - 특정 카테고리 조회
- `PUT /api/categories/{id}/` - 카테고리 수정
- `DELETE /api/categories/{id}/` - 카테고리 삭제

### 태그
- `GET /api/tags/` - 전체 태그 목록
- `POST /api/tags/` - 새 태그 생성
- `GET /api/tags/{id}/` - 특정 태그 조회
- `PUT /api/tags/{id}/` - 태그 수정
- `DELETE /api/tags/{id}/` - 태그 삭제

### 댓글
- `GET /api/comments/` - 전체 댓글 목록
- `POST /api/comments/` - 새 댓글 작성
- `GET /api/comments/{id}/` - 특정 댓글 조회
- `PUT /api/comments/{id}/` - 댓글 수정
- `DELETE /api/comments/{id}/` - 댓글 삭제

## 설치 및 실행

1. 저장소 클론:
```bash
git clone <저장소-URL>
cd I-eung
```

2. 환경 변수 설정:
```bash
cp .env.example .env
```

3. `.env` 파일의 환경 변수를 적절한 값으로 수정

4. Docker Compose로 실행:
```bash
docker compose up --build
```

또는 로컬에서 SQLite로 실행:
```bash
cd Recommand
python manage.py migrate
python manage.py runserver
```

## 인증

API는 Django REST framework의 세션 인증을 사용합니다:

1. `/api-auth/login/` 접속
2. 로그인 정보 입력
3. 인증된 세션으로 API 요청 가능

## 추천 시스템

추천 시스템은 다음 요소들을 고려하여 게시글을 추천합니다:
- 사용자가 좋아요한 게시글
- 좋아요한 게시글의 태그
- 좋아요한 게시글의 카테고리
- 게시글 평점
- 게시글 인기도(좋아요 수)

게시글 순위 결정 요소:
1. 관련성 점수(일치하는 태그와 카테고리)
2. 평균 평점
3. 좋아요 수

## 개발 환경

### 요구사항
- Python 3.12 이상
- Django 4.2
- Django REST framework
- MySQL (Docker 설정용)
- Docker 및 Docker Compose (선택사항)

### 프로젝트 구조
```
Recommand/
├── articles/                 # 메인 앱
│   ├── models.py            # 데이터 모델
│   ├── serializers.py       # API 시리얼라이저
│   ├── views.py             # API 뷰
│   └── admin.py             # 관리자 인터페이스
├── Recommand/               # 프로젝트 설정
│   ├── settings.py          # Django 설정
│   └── urls.py              # URL 라우팅
└── manage.py                # Django CLI

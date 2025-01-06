# Recommand Project

## 프로젝트 소개
Django 기반의 추천 시스템 웹 애플리케이션입니다.

## 기술 스택
- Python 3.12
- Django 4.2
- MySQL 8.0
- Docker & Docker Compose

## 프로젝트 구조
```
프로젝트 루트/
├── Recommand/              # Django 프로젝트
│   ├── Recommand/         # 프로젝트 설정
│   ├── articles/         # 앱
│   └── Dockerfile        # Django 서비스 Dockerfile
├── docker-compose.yml    # Docker Compose 설정
├── requirements.txt      # Python 의존성 패키지
└── .env.example         # 환경 변수 템플릿
```

## 개발 환경 설정

### 사전 요구사항
- Docker
- Docker Compose

### 환경 변수 설정
1. `.env.example` 파일을 `.env`로 복사하고 필요한 값을 설정합니다:
```bash
cp .env.example .env
```

2. `.env` 파일을 열고 다음 값들을 설정합니다:
```
DJANGO_SECRET_KEY=your_django_secret_key_here
DEBUG=1
DB_NAME=recommand_db
DB_USER=recommand_user
DB_PASSWORD=your_db_password_here
MYSQL_ROOT_PASSWORD=your_mysql_root_password_here
```

### Docker로 실행하기

1. 이미지 빌드 및 컨테이너 실행:
```bash
docker-compose up --build
```

2. 데이터베이스 마이그레이션:
```bash
# 새 터미널에서
docker-compose exec django python manage.py migrate
```

3. 관리자 계정 생성 (선택사항):
```bash
docker-compose exec django python manage.py createsuperuser
```

### 서비스 접속
- Django 애플리케이션: http://localhost:8000
- Django 관리자 페이지: http://localhost:8000/admin
- MySQL 데이터베이스: localhost:3306

### 개발 명령어

데이터베이스 마이그레이션 생성:
```bash
docker-compose exec django python manage.py makemigrations
```

마이그레이션 적용:
```bash
docker-compose exec django python manage.py migrate
```

Django 쉘 실행:
```bash
docker-compose exec django python manage.py shell
```

MySQL 쉘 접속:
```bash
docker-compose exec db mysql -u root -p
```

로그 확인:
```bash
docker-compose logs -f
```

서비스 중지:
```bash
docker-compose down
```

데이터베이스 볼륨을 포함한 전체 중지:
```bash
docker-compose down -v
```

## 개발 가이드라인
- 코드 스타일은 PEP 8을 따릅니다
- 새로운 기능은 별도의 브랜치에서 개발합니다
- 커밋 메시지는 명확하게 작성합니다
- API 문서화는 DRF(Django REST Framework)의 기능을 활용합니다

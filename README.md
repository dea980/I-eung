# 레시피 추천 시스템

## 시작하기

이 프로젝트는 Django와 Django REST Framework를 사용하여 구현된 레시피 추천 시스템입니다.

### 필수 요구사항

- Python 3.12 이상
- pip (Python 패키지 관리자)

### 설치 방법

1. 필요한 패키지 설치:
```bash
pip install django djangorestframework django-cors-headers mysqlclient python-dotenv Pillow
```

2. 환경 변수 설정:
   - `.env.example` 파일을 `.env`로 복사하고 필요한 설정을 입력합니다.
```bash
cp .env.example .env
```

3. 데이터베이스 마이그레이션:
```bash
cd Recommand
python manage.py migrate
```

4. 관리자 계정 생성:
```bash
python manage.py createsuperuser
```

5. 샘플 레시피 데이터 로드:
```bash
python manage.py load_recipes
```

### 실행 방법

개발 서버 실행:
```bash
python manage.py runserver
```

서버는 기본적으로 http://127.0.0.1:8000/ 에서 실행됩니다.

## API 엔드포인트

### 기본 엔드포인트
- API 루트: `/api/`
- 관리자 인터페이스: `/admin/`

### 레시피 관련 엔드포인트
- 레시피 목록: `/api/recipes/`
  - 난이도별 필터링: `/api/recipes/?difficulty=easy`
  - 조리시간별 필터링: `/api/recipes/?max_time=30`
- 카테고리: `/api/categories/`
- 재료: `/api/ingredients/`
- 조리도구: `/api/cooking-tools/`

### 장바구니 기능
- 장바구니: `/api/cart/`
- 장바구니 비우기: POST `/api/cart/clear/`

### 추천 시스템
- 사용자 선호도: `/api/preferences/`
- 레시피 상호작용: `/api/recipe-interactions/`
- 추천 받기: `/api/recommendations/`

## 디버깅

### 일반적인 문제 해결

1. 서버가 시작되지 않는 경우:
   - 포트가 이미 사용 중인지 확인
   ```bash
   pkill -f runserver
   python manage.py runserver
   ```
   - 환경 변수가 제대로 설정되었는지 확인

2. 데이터베이스 관련 오류:
   - 마이그레이션이 제대로 적용되었는지 확인
   ```bash
   python manage.py showmigrations
   python manage.py migrate
   ```

3. 정적 파일 로드 실패:
   - 정적 파일 수집
   ```bash
   python manage.py collectstatic
   ```

### 로깅 설정

`settings.py`에서 로깅 레벨을 DEBUG로 설정하여 자세한 로그를 확인할 수 있습니다:

```python
DEBUG = True
```

### API 테스트

1. 브라우저에서 테스트:
   - Django REST Framework의 브라우저블 API 인터페이스 사용
   - 각 엔드포인트에서 직접 API 테스트 가능

2. 인증이 필요한 엔드포인트:
   - 관리자 계정으로 로그인 필요
   - 브라우저에서 `/admin/`으로 접속하여 로그인

3. JSON 형식으로 응답 받기:
   - URL 끝에 `?format=json` 추가
   예: `http://127.0.0.1:8000/api/recipes/?format=json`

## Docker 환경 (선택사항)

Docker를 사용하여 실행하려면:

```bash
docker-compose up --build
```

## 주의사항

- 개발 환경에서만 `DEBUG = True` 사용
- 실제 운영 환경에서는 보안을 위해 `DEBUG = False`로 설정
- 중요한 환경 변수는 반드시 `.env` 파일에 설정
- API 키와 비밀번호는 절대 GitHub에 커밋하지 않도록 주의

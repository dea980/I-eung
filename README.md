# 레시피 관리 시스템 API 문서

## 개요
이 프로젝트는 사용자들이 레시피를 관리하고, 재료를 기반으로 레시피를 추천받으며, 장보기 목록을 관리할 수 있는 API 시스템입니다.

## 기술 스택
- FastAPI: 웹 프레임워크
- SQLAlchemy: ORM
- MySQL: 데이터베이스
- Pydantic: 데이터 검증

## 주요 기능

### 1. 사용자 관리
- 사용자 등록
- 즐겨찾기 레시피 관리
- 개인 장보기 목록 관리

### 2. 레시피 관리
- 레시피 등록
- 레시피에 필요한 재료와 도구 관리
- AI 기반 레시피 생성 (준비 중)

### 3. 재료 및 도구 관리
- 재료 등록 (이름, 가격, 단위)
- 요리 도구 등록
- 재료별 가격 정보 관리

### 4. 레시피 추천 시스템
- 보유 재료 기반 레시피 추천
- 보유 도구 기반 레시피 추천
- 부족한 재료 정보 제공

### 5. 장보기 목록
- 필요한 재료 추가
- 수량 및 단위 관리

## API 엔드포인트

### 사용자 관리
- POST /users/: 새 사용자 등록
- POST /users/{user_id}/favorites/{recipe_id}: 즐겨찾기에 레시피 추가
- POST /users/{user_id}/shopping-list: 장보기 목록에 아이템 추가

### 레시피 관리
- POST /recipes/: 새 레시피 등록
- POST /recipes/recommend: 레시피 추천 받기
- POST /recipes/generate: AI 레시피 생성 (개발 중)

### 재료 및 도구 관리
- POST /ingredients/: 새 재료 등록
- POST /tools/: 새 도구 등록

## 데이터베이스 구조

### 주요 테이블
1. users: 사용자 정보
2. recipes: 레시피 정보
3. ingredients: 재료 정보
4. tools: 도구 정보

### 연결 테이블
1. favorites: 사용자의 즐겨찾기 레시피
2. shopping_list: 사용자의 장보기 목록
3. recipe_ingredients: 레시피별 필요 재료
4. recipe_tools: 레시피별 필요 도구

## 설치 및 실행 방법

1. 데이터베이스 설정
```sql
CREATE DATABASE recipe_db;
```

2. 환경 설정
```bash
# 데이터베이스 접속 정보 설정
DATABASE_URL="mysql+pymysql://user:password@localhost/recipe_db"
```

3. 서버 실행
```bash
python main.py
```

## 참고사항
- 모든 API 응답은 JSON 형식입니다.
- 에러 메시지는 한글로 제공됩니다.
- AI 레시피 생성 기능은 현재 기본 템플릿만 제공하며, 추후 AI 서비스와 연동될 예정입니다.

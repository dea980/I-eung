from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests

app = FastAPI()

# 데이터베이스 설정
DATABASE_URL = "mysql+mysqlconnector://user:1234@localhost/todos"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 사용자 모델 정의
class User(Base):
    __tablename__ = "users"
    order_id = Column(Integer, unique=True)  # 가입 순서 번호 추가
    user_key = Column(String(255), primary_key=True, index=True)  # id를 user_key로 변경
    name = Column(String(255))
    email = Column(String(255))
    status = Column(String(50))  # 사용자 상태 추가

@app.get("/")
def health_check_handler():
    return {"status": "ok"}

@app.get("/users", status_code=200)
def get_all_users(session: Session = Depends(SessionLocal)):
    db_users = session.query(User).all()
    return [{"id": user.id, "name": user.name, "email": user.email, "status": user.status} for user in db_users]

@app.get("/user/{user_id}", status_code=200)
def get_user(user_id: str, session: Session = Depends(SessionLocal)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"id": user.id, "name": user.name, "email": user.email, "status": user.status}

@app.post("/users", status_code=201)
def create_user(user: User, session: Session = Depends(SessionLocal)):
    # 가장 높은 order_id 찾기
    last_order = session.query(User).order_by(User.order_id.desc()).first()
    user.order_id = (last_order.order_id + 1) if last_order else 1  # 1부터 시작

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email, "status": user.status, "order_id": user.order_id}

@app.patch("/user/{user_id}/status", status_code=200)
def update_user_status(user_id: str, status: str = Body(..., embed=True), session: Session = Depends(SessionLocal)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    user.status = status
    session.commit()
    session.refresh(user)
    return {"detail": "User status updated successfully", "user": {"id": user.id, "name": user.name, "email": user.email, "status": user.status}}

@app.delete("/user/{user_id}", status_code=204)
def delete_user(user_id: str, session: Session = Depends(SessionLocal)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    session.delete(user)
    session.commit()
    return None 

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 

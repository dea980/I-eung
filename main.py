from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# 데이터베이스 설정
DATABASE_URL = "mysql+pymysql://user:password@localhost/recipe_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 연결 테이블
# 즐겨찾기: 사용자와 레시피 간의 다대다 관계
favorites = Table('favorites', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id'))
)

# 장보기 목록: 사용자와 재료 간의 다대다 관계
shopping_list = Table('shopping_list', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id')),
    Column('quantity', Float),  # 수량
    Column('unit', String(50))  # 단위
)

# 데이터베이스 모델
# 사용자 모델
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    favorite_recipes = relationship("Recipe", secondary=favorites, back_populates="favorited_by")  # 즐겨찾기한 레시피들
    shopping_items = relationship("Ingredient", secondary=shopping_list)  # 장보기 목록의 재료들

# 재료 모델
class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    price = Column(Float, nullable=True)  # 단위당 가격
    unit = Column(String(50))  # 단위 (예: "kg", "개", "ml")
    recipes = relationship("RecipeIngredient", back_populates="ingredient")

# 도구 모델
class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    recipes = relationship("RecipeTool", back_populates="tool")

# 레시피 모델
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    instructions = Column(String(2000))  # 조리 방법
    cooking_time = Column(Integer)  # 조리 시간 (분)
    difficulty = Column(String(50))  # 난이도
    ingredients = relationship("RecipeIngredient", back_populates="recipe")  # 레시피에 필요한 재료들
    tools = relationship("RecipeTool", back_populates="recipe")  # 레시피에 필요한 도구들
    favorited_by = relationship("User", secondary=favorites, back_populates="favorite_recipes")  # 이 레시피를 즐겨찾기한 사용자들
    is_ai_generated = Column(Integer, default=0)  # AI 생성 여부

# 레시피-재료 연결 모델
class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float)  # 필요한 재료의 양
    unit = Column(String(50))  # 단위
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes")

# 레시피-도구 연결 모델
class RecipeTool(Base):
    __tablename__ = "recipe_tools"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    tool_id = Column(Integer, ForeignKey("tools.id"))
    recipe = relationship("Recipe", back_populates="tools")
    tool = relationship("Tool", back_populates="recipes")

# Pydantic 모델 (API 요청/응답 데이터 검증용)
# 재료 기본 모델
class IngredientBase(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None

# 재료 생성 모델
class IngredientCreate(IngredientBase):
    price: Optional[float] = None

# 도구 기본 모델
class ToolBase(BaseModel):
    name: str

# 도구 생성 모델
class ToolCreate(ToolBase):
    pass

# 레시피 기본 모델
class RecipeBase(BaseModel):
    name: str
    instructions: str
    cooking_time: int
    difficulty: str

# 레시피 생성 모델
class RecipeCreate(RecipeBase):
    ingredients: List[IngredientBase]
    tools: List[str]

# 사용자 기본 모델
class UserBase(BaseModel):
    name: str
    email: str

# 사용자 생성 모델
class UserCreate(UserBase):
    password: str

# 장보기 목록 아이템 모델
class ShoppingListItem(BaseModel):
    ingredient_id: int
    quantity: float
    unit: str

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 라우트
# 사용자 생성
@app.post("/users/", response_model=UserBase)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
    new_user = User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 재료 생성
@app.post("/ingredients/")
def create_ingredient(ingredient: IngredientCreate, db: SessionLocal = Depends(get_db)):
    db_ingredient = db.query(Ingredient).filter(Ingredient.name == ingredient.name).first()
    if db_ingredient:
        raise HTTPException(status_code=400, detail="이미 존재하는 재료입니다")
    new_ingredient = Ingredient(
        name=ingredient.name,
        price=ingredient.price,
        unit=ingredient.unit
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

# 도구 생성
@app.post("/tools/")
def create_tool(tool: ToolCreate, db: SessionLocal = Depends(get_db)):
    db_tool = db.query(Tool).filter(Tool.name == tool.name).first()
    if db_tool:
        raise HTTPException(status_code=400, detail="이미 존재하는 도구입니다")
    new_tool = Tool(name=tool.name)
    db.add(new_tool)
    db.commit()
    db.refresh(new_tool)
    return new_tool

# 레시피 생성
@app.post("/recipes/")
def create_recipe(recipe: RecipeCreate, db: SessionLocal = Depends(get_db)):
    # 레시피 기본 정보 생성
    new_recipe = Recipe(
        name=recipe.name,
        instructions=recipe.instructions,
        cooking_time=recipe.cooking_time,
        difficulty=recipe.difficulty
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # 재료 추가
    for ingredient_data in recipe.ingredients:
        ingredient = db.query(Ingredient).filter(Ingredient.name == ingredient_data.name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_data.name, unit=ingredient_data.unit)
            db.add(ingredient)
            db.commit()
            db.refresh(ingredient)
        
        recipe_ingredient = RecipeIngredient(
            recipe_id=new_recipe.id,
            ingredient_id=ingredient.id,
            quantity=ingredient_data.quantity,
            unit=ingredient_data.unit
        )
        db.add(recipe_ingredient)

    # 도구 추가
    for tool_name in recipe.tools:
        tool = db.query(Tool).filter(Tool.name == tool_name).first()
        if not tool:
            tool = Tool(name=tool_name)
            db.add(tool)
            db.commit()
            db.refresh(tool)
        
        recipe_tool = RecipeTool(recipe_id=new_recipe.id, tool_id=tool.id)
        db.add(recipe_tool)

    db.commit()
    return new_recipe

# 레시피 추천
@app.post("/recipes/recommend")
def recommend_recipes(ingredients: List[IngredientBase], tools: List[str], db: SessionLocal = Depends(get_db)):
    # 모든 레시피 가져오기
    recipes = db.query(Recipe).all()
    recommendations = []
    
    for recipe in recipes:
        # 사용자가 가진 재료로 만들 수 있는지 확인
        has_ingredients = True
        missing_ingredients = []
        
        for recipe_ingredient in recipe.ingredients:
            ingredient_found = False
            for user_ingredient in ingredients:
                if recipe_ingredient.ingredient.name == user_ingredient.name:
                    if not user_ingredient.quantity or user_ingredient.quantity >= recipe_ingredient.quantity:
                        ingredient_found = True
                        break
            if not ingredient_found:
                has_ingredients = False
                missing_ingredients.append({
                    "name": recipe_ingredient.ingredient.name,
                    "quantity": recipe_ingredient.quantity,
                    "unit": recipe_ingredient.unit,
                    "price": recipe_ingredient.ingredient.price
                })
        
        # 사용자가 필요한 도구를 가지고 있는지 확인
        has_tools = True
        missing_tools = []
        
        for recipe_tool in recipe.tools:
            if recipe_tool.tool.name not in tools:
                has_tools = False
                missing_tools.append(recipe_tool.tool.name)
        
        recommendations.append({
            "recipe": recipe,
            "has_all_ingredients": has_ingredients,
            "missing_ingredients": missing_ingredients,
            "has_all_tools": has_tools,
            "missing_tools": missing_tools
        })
    
    # 부족한 재료와 도구가 적은 순서로 정렬
    recommendations.sort(key=lambda x: (
        len(x["missing_ingredients"]) + len(x["missing_tools"]),
        0 if x["has_all_ingredients"] else 1,
        0 if x["has_all_tools"] else 1
    ))
    
    return recommendations[:5]  # 상위 5개 추천 반환

# 즐겨찾기에 레시피 추가
@app.post("/users/{user_id}/favorites/{recipe_id}")
def add_to_favorites(user_id: int, recipe_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="레시피를 찾을 수 없습니다")
    
    user.favorite_recipes.append(recipe)
    db.commit()
    return {"message": "레시피가 즐겨찾기에 추가되었습니다"}

# 장보기 목록에 아이템 추가
@app.post("/users/{user_id}/shopping-list")
def add_to_shopping_list(
    user_id: int,
    item: ShoppingListItem,
    db: SessionLocal = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    ingredient = db.query(Ingredient).filter(Ingredient.id == item.ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="재료를 찾을 수 없습니다")
    
    # 장보기 목록에 추가
    stmt = shopping_list.insert().values(
        user_id=user_id,
        ingredient_id=item.ingredient_id,
        quantity=item.quantity,
        unit=item.unit
    )
    db.execute(stmt)
    db.commit()
    
    return {"message": "장보기 목록에 아이템이 추가되었습니다"}

# AI 레시피 생성
@app.post("/recipes/generate")
def generate_recipe(ingredients: List[str], db: SessionLocal = Depends(get_db)):
    # AI 레시피 생성을 위한 플레이스홀더
    # 실제 구현에서는 AI 서비스와 통합해야 함
    # 현재는 간단한 템플릿 반환
    
    recipe_name = f"AI가 생성한 레시피: {', '.join(ingredients[:3])}"
    instructions = f"""
    다음 재료를 사용한 AI 생성 레시피입니다: {', '.join(ingredients)}
    
    1. 모든 재료를 준비합니다
    2. 재료를 섞습니다
    3. 적절한 방법으로 조리합니다
    4. 완성되면 맛있게 드세요!
    """
    
    new_recipe = Recipe(
        name=recipe_name,
        instructions=instructions,
        cooking_time=30,
        difficulty="중간",
        is_ai_generated=1
    )
    
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    
    return new_recipe

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

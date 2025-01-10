import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create base class for declarative models
Base = declarative_base()

# Define Recipe model
class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    recipe_no = Column(String(20))
    title = Column(String(200))
    cooking_name = Column(String(100))
    registrant_id = Column(String(50))
    registrant_name = Column(String(50))
    view_count = Column(Integer)
    recommend_count = Column(Integer)
    scrap_count = Column(Integer)
    cooking_method = Column(String(50))
    cooking_status = Column(String(50))
    ingredients_type = Column(String(50))
    dish_type = Column(String(50))
    description = Column(Text)
    ingredients = Column(Text)
    servings = Column(String(50))
    difficulty = Column(String(50))
    cooking_time = Column(String(50))
    reg_date = Column(String(50))

def load_recipes():
    # Read CSV file
    df = pd.read_csv('RECIPE_DATA.csv')
    
    # Create database engine
    engine = create_engine('sqlite:///recipes.db')
    
    # Create tables
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Process each row and insert into database
    for _, row in df.iterrows():
        recipe = Recipe(
            recipe_no=row['RCP_SNO'],
            title=row['RCP_TTL'],
            cooking_name=row['CKG_NM'],
            registrant_id=row['RGTR_ID'],
            registrant_name=row['RGTR_NM'],
            view_count=row['INQ_CNT'],
            recommend_count=row['RCMM_CNT'],
            scrap_count=row['SRAP_CNT'],
            cooking_method=row['CKG_MTH_ACTO_NM'],
            cooking_status=row['CKG_STA_ACTO_NM'],
            ingredients_type=row['CKG_MTRL_ACTO_NM'],
            dish_type=row['CKG_KND_ACTO_NM'],
            description=row['CKG_IPDC'],
            ingredients=row['CKG_MTRL_CN'],
            servings=row['CKG_INBUN_NM'],
            difficulty=row['CKG_DODF_NM'],
            cooking_time=row['CKG_TIME_NM'],
            reg_date=row['FIRST_REG_DT']
        )
        session.add(recipe)
    
    # Commit changes
    session.commit()
    session.close()

if __name__ == '__main__':
    load_recipes()
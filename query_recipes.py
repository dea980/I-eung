from sqlalchemy import create_engine, text

# Create database connection
engine = create_engine('sqlite:///recipes.db')

# Query data and verify
with engine.connect() as connection:
    # Execute query to get first 5 recipes
    result = connection.execute(text("SELECT * FROM recipes LIMIT 5"))
    
    # Print each row
    for row in result:
        print(row)
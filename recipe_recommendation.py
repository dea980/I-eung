import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data from CSV
df01 = pd.read_csv('RECIPE_DATA.csv')

# Convert to dictionary format with list orientation
data = df01.to_dict(orient='list')

# Create DataFrame and remove any NA values
recipes_df = pd.DataFrame(data).dropna()

# Initialize Korean text processor
okt = Okt()

def preprocess_ingredients(text):
    # Tokenize and normalize Korean text
    tokens = okt.normalize(text)
    tokens = okt.phrases(tokens)
    return ' '.join(tokens)

def recommend_recipes(user_ingredients, recipes_df):
    # Preprocess user ingredients
    user_ingredients = preprocess_ingredients(user_ingredients)
    
    # Preprocess recipe ingredients
    recipes_df['processed_ingredients'] = recipes_df['CKG_MTRL_CN'].apply(preprocess_ingredients)
    
    # Create TF-IDF vectorizer
    tfidf = TfidfVectorizer()
    
    # Combine user ingredients with recipe ingredients for fitting
    all_ingredients = [user_ingredients] + recipes_df['processed_ingredients'].tolist()
    tfidf_matrix = tfidf.fit_transform(all_ingredients)
    
    # Calculate similarity between user ingredients and all recipes
    user_vector = tfidf_matrix[0:1]
    recipe_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(user_vector, recipe_vectors)[0]
    
    # Get indices of top similar recipes
    top_indices = similarities.argsort()[::-1][:10]  # Get top 10 recipes
    
    # Create result list with recipe information
    recommended_recipes = []
    for idx in top_indices:
        recommended_recipes.append({
            'recipe_name': recipes_df.iloc[idx]['CKG_NM'],
            'ingredients': recipes_df.iloc[idx]['CKG_MTRL_CN'],
            'sdescription': recipes_df.iloc[idx]['CKG_IPDC']
        })
    
    return recommended_recipes

# Example usage
user_ingredients_list = ['대파', '마늘', '계란', '고추장']
user_ingredients = ' '.join(user_ingredients_list)
recommended_recipes = recommend_recipes(user_ingredients, recipes_df)
recommended_recipes_dataframe = pd.DataFrame(recommended_recipes[['recipe_name', 'ingredients', 'sdescription']])

print(f"검색단어:{user_ingredients}")
recommended_recipes_dataframe.head(10)
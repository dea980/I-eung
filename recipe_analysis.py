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

# Function to preprocess ingredients text
def preprocess_ingredients(text):
    # Tokenize and normalize Korean text
    tokens = okt.normalize(text)
    tokens = okt.phrases(tokens)
    return ' '.join(tokens)

# Preprocess ingredients column
recipes_df['processed_ingredients'] = recipes_df['CKG_MTRL_CN'].apply(preprocess_ingredients)

# Create TF-IDF vectorizer
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(recipes_df['processed_ingredients'])

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recipe recommendations
def get_recommendations(idx, cosine_sim=cosine_sim):
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 similar recipes (excluding itself)
    recipe_indices = [i[0] for i in sim_scores]
    return recipes_df.iloc[recipe_indices][['RCP_TTL', 'CKG_MTRL_CN']]

# Example: Get recommendations for first recipe
print("Recommendations for:", recipes_df.iloc[0]['RCP_TTL'])
recommendations = get_recommendations(0)
print("\nRecommended recipes:")
print(recommendations)
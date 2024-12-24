
import pandas as pd
import sentencepiece as spm

# CSV 파일에서 데이터 불러오기
data = pd.read_csv('/Users/yoobmooyeol/Desktop/i-eung/data/TB_RECIPE_SEARCH-20231130-30.csv')

# 'ingredients' 열 추출
ingredients = data['ingredients']

# 'ingredients' 내용을 파일로 저장
with open('ingredients.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(ingredients))

# SentencePiece 모델 훈련
spm.SentencePieceTrainer.Train('--input=ingredients.txt --model_prefix=ingredients_sp --vocab_size=2000')

# SentencePiece 모델 로드
sp = spm.SentencePieceProcessor()
sp.load('ingredients_sp.model')

# 'ingredients' 열 토큰화
data['ingredients_tokenized'] = ingredients.apply(lambda x: sp.encode_as_pieces(x))
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. 임베딩 모델 로드
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. FAISS 벡터 DB 초기화
dimension = 384  # 모델 임베딩 차원
index = faiss.IndexFlatL2(dimension)

# 3. 벡터 추가 함수
def add_to_vector_db(texts: list[str]):
    vectors = embedding_model.encode(texts)
    index.add(np.array(vectors, dtype="float32"))

# 4. 유사 문장 검색
def search_similar(query: str, top_k: int = 3):
    query_vec = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_vec, dtype="float32"), top_k)
    return indices[0], distances[0]
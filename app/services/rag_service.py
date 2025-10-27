import re
from app.vectorstore import chroma_client, embedding_function

def split_text_into_chunks(text: str, max_len: int = 300):
    """문장을 청킹 단위로 나눠서 저장"""
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_len:
            current += " " + sentence
        else:
            chunks.append(current.strip())
            current = sentence
    if current:
        chunks.append(current.strip())

    return chunks


def store_feedback_with_chunking(feedback_id: int, feedback_text: str, emotion: str):
    """피드백을 청킹 후 각 chunk를 임베딩 저장"""
    chunks = split_text_into_chunks(feedback_text)
    for idx, chunk in enumerate(chunks):
        chroma_client.add_texts(
            texts=[chunk],
            metadatas=[{"feedback_id": feedback_id, "chunk_id": idx, "emotion": emotion}],
            ids=[f"{feedback_id}-{idx}"],
            embedding_function=embedding_function
        )

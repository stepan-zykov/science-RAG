
from decouple import config
from langchain_community.vectorstores import UpstashVectorStore
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from langchain_community.llms import YandexGPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

UPSTASH_VECTOR_REST_URL = config("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = config("UPSTASH_VECTOR_REST_TOKEN")
STORE_CONFIG = {
    "index_url": UPSTASH_VECTOR_REST_URL,
    "index_token": UPSTASH_VECTOR_REST_TOKEN}

YC_FOLDER_ID = config('YC_FOLDER_ID')
YC_API_KEY = config('YC_API_KEY')
YA_EMB_CONFIG = {
    "api_key": YC_API_KEY,
    "folder_id": YC_FOLDER_ID,
    "doc_model_name": "text-search-query"}

LLM_CONFIG = {
    "api_key": YC_API_KEY,
    "folder_id": YC_FOLDER_ID,
    "model_name": "yandexgpt-lite"}

embeddings = YandexGPTEmbeddings(**YA_EMB_CONFIG)
store = UpstashVectorStore(embedding=embeddings, **STORE_CONFIG)
llm = YandexGPT(**LLM_CONFIG)
parser = StrOutputParser()
retriever = store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 2})

message = """
Ответь на вопрос, используя только предоставленный контекст.
Вопрос: {question}
Контекст: {context}
"""
prompt = ChatPromptTemplate.from_messages([('human', message)])

def get_chain():
    return {'context': retriever, "question": RunnablePassthrough()} | prompt | llm | parser





import os
import warnings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

_db = None


def get_db():
    global _db

    if _db is None:
        loader = TextLoader("knowledge_base.md")
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=40
        )

        chunks = splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        _db = FAISS.from_documents(chunks, embeddings)

    return _db


def search_docs(query: str) -> str:
    db = get_db()
    docs = db.similarity_search(query, k=2)
    return "\n".join([doc.page_content for doc in docs])
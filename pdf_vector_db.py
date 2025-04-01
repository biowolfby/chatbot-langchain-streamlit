"""based on retrievers.ipynb
Original file is located at
    https://colab.research.google.com/drive/1-YfFkA6U5Y7YXnISuUAUYFvGW_BCl3C0
"""

from langchain_community.document_loaders import PyPDFLoader

file_path = "nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(f"Number of docs loaded from PDF file: {len(docs)}\n")
print(f"First page metadata: {docs[0].metadata}\n")
print(f"First page content btgining: {docs[0].page_content[:200]}\n")

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(f"Number of splits: {len(all_splits)}\n")

import getpass
import os
from dotenv import load_dotenv

load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

from langchain_mistralai import MistralAIEmbeddings

embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=mistral_api_key)

import time

vector_1 = embeddings.embed_query(all_splits[0].page_content)
print(f"Test embedding from first split\n")
print (f"Vector length: {len(vector_1)}\n")
print(f"Vector: {vector_1[:10]}\n") 

# | output: false
# | echo: false

from langchain_chroma import Chroma

vector_store = Chroma(embedding_function=embeddings, persist_directory="chroma_db")

# Ensure the vector store is persisted by setting the persist_directory during initialization
print("Vector store initialized with persistence enabled.")

# just becouse requests are limited to Mistral API
print(f"Adding all splits to vector store. Batching becouse of Mistral API limits\n")
batch_size = 15  # По 10 документов за раз
for i in range(0, len(all_splits), batch_size):
    batch = all_splits[i : i + batch_size]
    vector_store.add_documents(batch)
    print(i, "added")
    time.sleep(2)  # Даем API "отдохнуть"

#ids = vector_store.add_documents(documents=all_splits)

new_vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory="chroma_db",
)


print(f"Testing new vector store with query\n")
results = new_vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)

print(results[0])

# results = await vector_store.asimilarity_search("When was Nike incorporated?")

# print(results[0])

# Note that providers implement different scores; the score here
# is a distance metric that varies inversely with similarity.

time.sleep(2)
results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
doc, score = results[0]
print(f"Score: {score}\n")
print(doc)

# Return documents based on similarity to an embedded query:
time.sleep(2)
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")

results = vector_store.similarity_search_by_vector(embedding)
print(results[0])

# Retriver
# from typing import List

# from langchain_core.documents import Document
# from langchain_core.runnables import chain


# @chain
# def retriever(query: str) -> List[Document]:
#     return vector_store.similarity_search(query, k=1)

# time.sleep(5)
# retriever.batch(
#     [
#         "How many distribution centers does Nike have in the US?",
#         "When was Nike incorporated?",
#     ],
# )

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)

time.sleep(5)
retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)
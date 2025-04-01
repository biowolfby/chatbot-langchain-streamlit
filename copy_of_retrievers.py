"""based on retrievers.ipynb
Original file is located at
    https://colab.research.google.com/drive/1-YfFkA6U5Y7YXnISuUAUYFvGW_BCl3C0
"""

from langchain_community.document_loaders import PyPDFLoader

file_path = "nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))

print(f"{docs[0].page_content[:200]}\n")
print(docs[0].metadata)

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))

import getpass
import os
from dotenv import load_dotenv

load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

from langchain_mistralai import MistralAIEmbeddings

embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=mistral_api_key)

import time

vector_1 = embeddings.embed_query(all_splits[0].page_content)
time.sleep(1)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])

# | output: false
# | echo: false

from langchain_chroma import Chroma

vector_store = Chroma(embedding_function=embeddings)

# just becouse requests are limited to Mistral API
batch_size = 15  # По 10 документов за раз
for i in range(0, len(all_splits), batch_size):
    batch = all_splits[i : i + batch_size]
    vector_store.add_documents(batch)
    print(i, "added")
    time.sleep(2)  # Даем API "отдохнуть"

#ids = vector_store.add_documents(documents=all_splits)

results = vector_store.similarity_search(
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
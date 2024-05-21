# Getting the host running Ollama
import os
ollama_host = os.environ["OLLAMA_HOST"] or "localhost"
base_url = f"http://{ollama_host}:11434"

import gradio as gr
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

prompt = """
Your name is Mitra. You are an assistant for question-answering tasks for Mitra Robot customer support. 
You need to use the following pieces of retrieved context to answer the question. 
Use three sentences maximum and keep the answer concise. 
Answer only robot related questions and nothing else. If they ask something like biriyani bring them back to the conversation
"""

# 1. Load our DB
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db = Chroma(persist_directory="./doc_vectors", embedding_function=embeddings)
# llm = Ollama(model="qwen", base_url=base_url)
llm = ChatGroq(model_name="llama3-70b-8192")

# 2. set up our chat


def language_chat(message, history):
    docs = db.similarity_search(message)
    retrieved_string = "\n\n".join(doc.page_content for doc in docs)
    # print("I got these results for the message: ", message, retrieved_string)

    query = prompt + ". The context is: " + \
        retrieved_string + "The question is :" + \
        message

    print(history)
    # print(query)
    return llm.invoke(query).content


demo = gr.ChatInterface(
    language_chat, title="Mitra Robot RAG", theme='Taithrah/Minimal')

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")

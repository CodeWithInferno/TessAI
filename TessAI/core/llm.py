from langchain_ollama import OllamaLLM, OllamaEmbeddings

llm = OllamaLLM(model="llama3.2")
embedding = OllamaEmbeddings(model="llama3.2")

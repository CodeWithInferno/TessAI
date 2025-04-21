from langchain_ollama import OllamaLLM, OllamaEmbeddings

llm = OllamaLLM(model="deepseek-r1:8b")
embedding = OllamaEmbeddings(model="deepseek-r1:8b")

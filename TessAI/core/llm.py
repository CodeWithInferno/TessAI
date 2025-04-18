from langchain_ollama import OllamaLLM, OllamaEmbeddings

llm = OllamaLLM(model="deepseek-coder:6.7b")
embedding = OllamaEmbeddings(model="deepseek-coder:6.7b")

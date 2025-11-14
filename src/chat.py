from search import search_prompt
import os
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_postgres import PGVector

from dotenv import load_dotenv
load_dotenv()

def main():

    for k in ("OPENAI_API_KEY","DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    chain = search_prompt() | llm

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    # Get user input
    query = input("Faça sua pergunta: ")

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )
    results = store.similarity_search_with_score(query, k=10)


    # Extract page content from results (results is a list of tuples: (Document, score))
    contexto = "\n".join([doc.page_content for doc, score in results])

    result = chain.invoke({"pergunta": query, "contexto": contexto})

    print(f"\nPERGUNTA: {query}")
    print(f"RESPOSTA: {result.content}")

if __name__ == "__main__":
    main()
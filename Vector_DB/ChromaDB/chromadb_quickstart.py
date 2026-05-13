# ChromaDB quickstart example
import chromadb

def main():
    # 1. Initialize the ChromaDB client
    # By default, this runs an in-memory database
    client = chromadb.Client()

     #  # 1. Inicializar el cliente PERSISTENTE (guarda en disco)
     #  client = chromadb.PersistentClient(path="./chroma_data")

    # 2. Create a collection
    # Collections are where ChromaDB stores embeddings, documents, and metadata
    collection = client.create_collection(name="realpython_example")

    # 3. Add documents to the collection
    # ChromaDB uses the "all-MiniLM-L6-v2" model by default to create
    # text embeddings automatically in the background.
    collection.add(
        documents=[
            "Traditional Italian pizza is famous for its thin crust, fresh ingredients, and wood-fired ovens.",
            "Einstein's theory of relativity revolutionized our understanding of space and time.",
            "Climate change represents a significant threat to the planet's ecosystems.",
        ],
        metadatas=[
            {"topic": "food"},
            {"topic": "science"},
            {"topic": "environment"},
        ],
        ids=["id1", "id2", "id3"],  # Unique identifiers for each document
    )

    print("✅ Documents vectorized and successfully added to the collection.\n")

    # 4. Query the collection
    # We perform a semantic search using natural language
    #query_text = "Find me information about delicious food"
    query_text = "Find me information about Einstein"
    print(f"Searching for: '{query_text}'...\n")

    results = collection.query(
        query_texts=[query_text],
        n_results=1,  # Return only the most similar result (Top K)
    )

    # 5. Display the results
    print("--- Semantic Search Result ---")
    print(f"Document: {results['documents'][0][0]}")
    print(f"Distance: {results['distances'][0][0]:.4f} (Lower is more similar)")
    print(f"Metadata: {results['metadatas'][0][0]}")


if __name__ == "__main__":
    main()
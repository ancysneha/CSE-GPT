from rag_pipeline import setup_rag, ask_question

print("Loading documents... Please wait...")
index, chunks, metadata = setup_rag()
print("RAG system ready!")

while True:
    query = input("\nAsk: ")
    if query.lower() == "exit":
        break

    answer, sources = ask_question(query, index, chunks, metadata)

    print("\nAnswer:", answer)
    print("Sources:", list(set(sources)))
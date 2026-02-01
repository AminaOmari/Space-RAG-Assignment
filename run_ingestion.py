# Team: Amina O, Ossama Z, Smia I


import os
try:
    from langchain_community.document_loaders import WikipediaLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    # Define the directory for persistent storage
    PERSIST_DIRECTORY = "./chroma_db"

    topics = ["Space exploration", "NASA", "SpaceX", "Mars exploration", "International Space Station"]
    documents = []

    print("Loading documents from Wikipedia...")
    for topic in topics:
        try:
            loader = WikipediaLoader(query=topic, load_max_docs=1)
            docs = loader.load()
            documents.extend(docs)
            print(f"Loaded: {topic}")
        except Exception as e:
            print(f"Error loading {topic}: {e}")

    print(f"Total documents loaded: {len(documents)}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    splits = text_splitter.split_documents(documents)
    print(f"Created {len(splits)} chunks.")

    print("Initializing Embedding Model...")
    # Using a standard, small, efficient model for embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Indexing data into ChromaDB... (This might take a minute)")
    if os.path.exists(PERSIST_DIRECTORY):
        print("Removing old database to start fresh...")
        import shutil
        shutil.rmtree(PERSIST_DIRECTORY)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory=PERSIST_DIRECTORY
    )

    print("Done! Data indexed and saved to ./chroma_db")

except Exception as e:
    print(f"An error occurred: {e}")

from .DocumentLoader import DocumentLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore



class VectorStore:

    def __init__(self, document_dir: str,
                 embedding_model: str = "models/gemini-embedding-001") -> None:
        self.loader = DocumentLoader(document_dir)
        self.embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
        self.vector_store = InMemoryVectorStore(self.embeddings)

    def prepare_documents(self):
        print("Loading documents...")
        self.loader.load()

        print("Splitting documents...")
        self.loader.split()

    def get_vector_store(self):
        if not self.loader.splits:
            self.prepare_documents()
        
        print("Creating vector store...")
        self.vector_store.add_documents(documents=self.loader.splits)
        return self.vector_store
    
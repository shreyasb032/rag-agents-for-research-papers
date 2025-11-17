"""
Loads all the files into memory and splits them using 
the text splitter
"""

import glob
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document


class DocumentLoader:

    def __init__(self, dir_path: str,
                 chunk_size: int = 1000, chunk_overlap: int = 100) -> None:
        """
        Initializes the DocumentLoader with the directory path containing PDF files
        and text splitting parameters.
        Args:
            dir_path (str): Path to the directory containing PDF files.
            chunk_size (int): Size of each text chunk after splitting.
            chunk_overlap (int): Overlap size between consecutive text chunks.
        """
        self.dir_path = dir_path
        self.docs = []
        self.splits : List[Document] = []
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load(self):
        """
        Loads all PDF files from the specified directory into memory.
        """
        file_paths = glob.glob(f'{self.dir_path}/*.pdf')

        for file_path in file_paths:
            loader = PyMuPDFLoader(file_path)
            docs = loader.load()
            self.docs.extend(docs)

    def split(self):
        """
        Splits the loaded documents into smaller chunks using the text splitter.
        """
        if not len(self.docs):
            self.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=True
        )

        self.splits = text_splitter.split_documents(self.docs)


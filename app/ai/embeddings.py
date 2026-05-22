import os

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    Chroma
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

POLICY_DIR = "data/policies"

CHROMA_DIR = "data/chroma_db"


def load_documents():

    documents = []

    for file in os.listdir(POLICY_DIR):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(
                os.path.join(POLICY_DIR, file)
            )

            documents.extend(
                loader.load()
            )

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(
        documents
    )


def build_vector_database():

    print("Loading policy documents...")

    docs = load_documents()

    print("Splitting documents...")

    split_docs = split_documents(docs)

    print("Generating embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    vectorstore.persist()

    print("Vector database created.")


if __name__ == "__main__":

    build_vector_database()
from langchain_community.vectorstores import (
    Chroma
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

CHROMA_DIR = "data/chroma_db"


def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )


def retrieve_policy_context(query, k=3):

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    query = """
    Transactions exceeding approval thresholds
    without secondary authorization
    """

    docs = retrieve_policy_context(query)

    for i, doc in enumerate(docs):

        print(f"\nResult {i+1}\n")

        print(doc.page_content)
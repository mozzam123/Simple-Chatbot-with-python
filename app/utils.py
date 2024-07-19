import os
import pickle

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Multiple URLS Code from Chatgpt
def get_vectorstore_from_urls(urls):
    """Retrieve vector store from the given list of URLs.

    This function loads documents from the provided URLs,
    splits them into chunks & creates a vector store.

    Args:
        urls (list): The list of URLs of the documents.

    Returns:
        Chroma: The vector store created from the document chunks.
    """
    all_document_chunks = []

    # Iterate over each URL     
    for url in urls:
        # Get text-in documents
        loader = WebBaseLoader(url)
        document = loader.load()

        # Split the documents into chunks
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)

        # Add the chunks to the list of all chunks
        all_document_chunks.extend(document_chunks)

    # Create Vector-store from the combined chunks:
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(all_document_chunks, embeddings)
    
    return vector_store


def get_doc_from_urls(urls):
    """Retrieve vector store from the given list of URLs.

    This function loads documents from the provided URLs,
    splits them into chunks & creates a vector store.

    Args:
        urls (list): The list of URLs of the documents.

    Returns:
        Chroma: The vector store created from the document chunks.
    """
    all_document_chunks = []

    # Iterate over each URL     
    for url in urls:
        # Get text-in documents
        loader = WebBaseLoader(url)
        document = loader.load()

        # Split the documents into chunks
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)

        # Add the chunks to the list of all chunks
        all_document_chunks.extend(document_chunks)

    # # Create Vector-store from the combined chunks:
    # embeddings = OpenAIEmbeddings()
    # vector_store = Chroma.from_documents(all_document_chunks, embeddings)
    
    return document_chunks


def get_context_retriever_chain(vector_store):
    """Create a context retriever chain using the given vector store.

    This function creates a history-aware retriever chain
    using a vector store and a chat prompt template.

    Args:
        vector_store (Chroma): The vector store to use.

    Returns:
        RetrievalChain: The context retriever chain.
    """
    llm = ChatOpenAI()
    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query "
                 "to look up in order to get information relevant to "
                 "the conversation")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)    

    return retriever_chain


def get_conversational_rag_chain(retriever_chain):
    """Create a conversational RAG chain
    using the given context retriever chain.

    This function creates a conversational RAG chain
    using a context retriever chain and a chat prompt template.

    Args:
        retriever_chain (RetrievalChain): The context retriever chain.

    Returns:
        RetrievalChain: The conversational RAG chain.
    """
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Answer the user's questions based"
            " on the below context:\n\n{context}"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)


def get_response(user_input, vector_store, chat_history):
    """Get the response for the given user query.

    This function retrieves the response for the user query
    using the conversational RAG chain.

    Args:
        user_input (str): The user query.

    Returns:
        str: The response to the user query.
    """
     # Create Conversation Chain
    retriever_chain = get_context_retriever_chain(
        vector_store
        )
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    # Invoke conversational RAG chain
    inv_response = conversation_rag_chain.invoke({
          "chat_history": chat_history,
          "input": user_input
      })
    return inv_response['answer']


def serialize_vector_store(vector_store):
    """Serialize the vector store to a byte stream."""
    return pickle.dumps(vector_store)
    # with open(f"vector_stores/{botname}", 'wb') as file:
    #     pickle.dump(vector_store, file)
    # return f"vector_stores/{botname}"

def deserialize_vector_store(serialized_vector_store):
    """Deserialize the vector store from a byte stream."""\
    
    all_document_chunks = pickle.loads(serialized_vector_store)
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(all_document_chunks, embeddings)
    return vector_store
    # with open(f"vector_stores/{botname}", 'rb') as file:
    #     vector_store = pickle.load(file)
    # return vector_store
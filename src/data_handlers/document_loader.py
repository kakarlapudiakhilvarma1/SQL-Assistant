"""
Document loading and processing utilities for the Healthcare Database Request Assistant.
"""

import os
import pickle
import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.utils.config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, FAISS_INDEX_PATH


def load_documents(directory_path):
    """
    Load PDF documents from the specified directory.

    Args:
        directory_path (str): Path to the directory containing PDF files

    Returns:
        list: List of loaded documents or empty list if error occurs
    """
    try:
        loader = PyPDFDirectoryLoader(directory_path)
        docs = loader.load()
        return docs
    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")
        return []


def process_documents(docs):
    """
    Split documents into chunks for better processing.

    Args:
        docs (list): List of documents to process

    Returns:
        list: List of processed document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        is_separator_regex=False,
    )
    documents = text_splitter.split_documents(docs)
    return documents


def create_vectorstore(documents, save_local=True):
    """
    Create a vector store from documents using HuggingFace embeddings.

    Args:
        documents (list): List of document chunks to embed
        save_local (bool): Whether to save the vectorstore locally

    Returns:
        FAISS: Vector store containing document embeddings
    """
    try:
        # Initialize embeddings with additional parameters to avoid meta tensor issues
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},  # Force CPU usage to avoid CUDA/meta tensor issues
            encode_kwargs={'normalize_embeddings': True}  # Ensure embeddings are normalized
        )
        vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)

        # Save the vectorstore locally if requested
        if save_local:
            save_vectorstore(vectorstore)

        return vectorstore
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        # Fallback to a simpler initialization if the first attempt fails
        try:
            st.info("Trying alternative embedding initialization...")
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)

            if save_local:
                save_vectorstore(vectorstore)

            return vectorstore
        except Exception as e2:
            st.error(f"Fallback embedding initialization also failed: {str(e2)}")
            return None


def save_vectorstore(vectorstore):
    """
    Save the vectorstore to disk.

    Args:
        vectorstore (FAISS): The vectorstore to save
    """
    try:
        vectorstore.save_local(FAISS_INDEX_PATH)
        st.success("Vector index saved successfully!")
    except Exception as e:
        st.error(f"Error saving vector index: {str(e)}")


def load_vectorstore():
    """
    Load the vectorstore from disk if it exists.

    Returns:
        FAISS or None: The loaded vectorstore or None if it doesn't exist
    """
    try:
        if os.path.exists(f"{FAISS_INDEX_PATH}.faiss"):
            # Initialize embeddings with additional parameters to avoid meta tensor issues
            embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},  # Force CPU usage to avoid CUDA/meta tensor issues
                encode_kwargs={'normalize_embeddings': True}  # Ensure embeddings are normalized
            )
            vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings)
            st.success("Loaded existing vector index!")
            return vectorstore
        return None
    except Exception as e:
        st.error(f"Error loading vector index: {str(e)}")
        # Try fallback method
        try:
            if os.path.exists(f"{FAISS_INDEX_PATH}.faiss"):
                st.info("Trying alternative embedding initialization for loading...")
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings)
                st.success("Loaded existing vector index with alternative method!")
                return vectorstore
        except Exception as e2:
            st.error(f"Fallback loading also failed: {str(e2)}")
        return None


def reset_vectorstore():
    """
    Delete the saved vectorstore files.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if os.path.exists(f"{FAISS_INDEX_PATH}.faiss"):
            os.remove(f"{FAISS_INDEX_PATH}.faiss")
        if os.path.exists(f"{FAISS_INDEX_PATH}.pkl"):
            os.remove(f"{FAISS_INDEX_PATH}.pkl")
        st.success("Vector index reset successfully!")
        return True
    except Exception as e:
        st.error(f"Error resetting vector index: {str(e)}")
        return False

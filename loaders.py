import os
from time import sleep
import streamlit as st
from langchain_community.document_loaders import (
    WebBaseLoader,
    YoutubeLoader, 
    CSVLoader, 
    PyPDFLoader, 
    TextLoader
)
from fake_useragent import UserAgent

def carrega_pdf(nome_arquivo):
    pasta = os.getcwd()
    caminho_completo = os.path.join(pasta, "Arquivos PDF",nome_arquivo)
    loader = PyPDFLoader(caminho_completo)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carregar_pdf_import(caminho):
    loader = PyPDFLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

# def carrega_pdf(pasta):
#     documentos = []
#     arquivos_carregados = []

#     for nome_arquivo in os.listdir(pasta):
#         if nome_arquivo.lower().endswith(".pdf"):
#             caminho_completo = os.path.join(pasta, nome_arquivo)
#             loader = PyPDFLoader(caminho_completo)
#             documentos.extend(loader.load())
#             arquivos_carregados.append(nome_arquivo)

#     documento = '\n\n'.join([doc.page_content for doc in documentos])
#     st.success(f"{len(arquivos_carregados)} PDFs carregados: {', '.join(arquivos_carregados)}")
#     return documento


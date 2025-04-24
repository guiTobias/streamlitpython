import tempfile

import streamlit as st
from langchain.memory import ConversationBufferMemory

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from loaders import *


TIPOS_ARQUIVOS_VALIDOS = []

CONFIG_MODELOS = {'Groq': 
                        {'modelos': ['llama-3.3-70b-versatile','llama3-70b-8192', 'gemma2-9b-it', 'whisper-large-v3-turbo','deepseek-r1-distill-llama-70b','compound-beta-mini','compound-beta'],
                         'chat': ChatGroq},
                  }

MEMORIA = ConversationBufferMemory()

for nome_arquivo in os.listdir("D:\OneDrive\Documents\Guilherme\python\ORACULO\Arquivos PDF"):
        if nome_arquivo.lower().endswith(".pdf"):
            TIPOS_ARQUIVOS_VALIDOS.append(nome_arquivo)

ORIGEM_ARQUIVOS = ['Importar']

def carrega_arquivos(tipo_arquivo, arquivo):
    if tipo_arquivo == 'Local':
        documento = carrega_pdf(arquivo)
    else:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carregar_pdf_import(nome_temp)

    return documento
            

def carrega_modelo(provedor, modelo, api_key, arquivo, tipo_arquivo):

    documento = carrega_arquivos(tipo_arquivo, arquivo)

    # documento = carrega_pdf(r"D:\OneDrive\Documents\Guilherme\python\ORACULO\Arquivos PDF")

    documento = documento[:15000]  # exemplo: limitar a 15k caracteres

    system_message = '''Você é um assistente amigável, instrutor de procedimentos chamado Prof.
    Você possui acesso às seguintes informações vindas 
    desses documentos da pasta: 

    ####
    {}
    ####

    Utilize as informações fornecidas para basear as suas respostas.

    Sempre que houver $ na sua saída, substita por Valor.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Prof!'''.format(documento)

    print(system_message)

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])
    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat

    st.session_state['chain'] = chain

def pagina_chat():
    st.header('👩‍🏫Bem-vindo ao Teacher', divider=True)

    chain = st.session_state.get('chain')
    if chain is None:
        st.error('Carregue o Teacher')
        st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input('Fale com o Teacher')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            'input': input_usuario, 
            'chat_history': memoria.buffer_as_messages
            }))
        
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

def sidebar():
    tabs = st.tabs(['Procedimentos'])
    with tabs[0]:
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS['Groq']['modelos'])
        api_key = st.text_input(
            f'Adicione a api key',
            value=st.session_state.get(f'api_key_Groq'))
        st.session_state[f'api_key_Groq'] = api_key
        tipo_arquivo = st.selectbox('Selecione um Procedimento', ORIGEM_ARQUIVOS)
        
        if tipo_arquivo == 'Local': 
            arquivo = st.selectbox('Selecione um Procedimento', TIPOS_ARQUIVOS_VALIDOS)
        else:
            arquivo = st.file_uploader('Faça o upload do arquivo pdf', type=['.pdf'])
    if st.button('Inicializar', use_container_width=True):
        carrega_modelo('Groq', modelo, api_key, arquivo, tipo_arquivo)
    if st.button('Apagar Histórico de Conversa', use_container_width=True):
        st.session_state['memoria'] = MEMORIA

def main():
    with st.sidebar:
        sidebar()
    pagina_chat()


if __name__ == '__main__':
    main()
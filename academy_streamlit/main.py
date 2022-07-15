## Importando bibliotecas necessárias
import os
os.chdir('./') # Necessário para que eu consiga encontrar o diretório raiz da aplicação

import streamlit as st
import time
from classe.model import ModelTitanic

## Necessário para ajustar o espaçamento no topo da aplicação
st.markdown("""
<style>.block-container {padding-top: 2rem;}</style>
""", unsafe_allow_html = True)

## Definição do cabeçalho (título, banner e componente de música)
header_col1, header_col2 = st.columns(2) 
with header_col1:
    st.title('MJV Academy')

with header_col2:
    ## Necessário para abrir arquivo de áudio
    audio_file = open('./files/titanic_soundtrack.mp3', 'rb')
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mp3')
    ## Necessário para ajustar o posicionamento e tamanho do componente de música
    st.markdown("""
    <style>
    .css-keje6w {display: flex; align-items: center;}
    .stAudio {position: absolute; height: 2rem; margin-top: 0.5rem;}
    </style>
    """, unsafe_allow_html = True)

st.image('./files/banner.jpg')

## Definição do texto de resumo da história
descricao = """
O **RMS Titanic** começou a ser construído em março de 1909 e seu lançamento ao 
mar ocorreu em maio de 1911. Ele foi pensado para ser o navio mais luxuoso 
e mais seguro de sua época, gerando lendas que era supostamente 'inafundável'.

A embarcação partiu em sua viagem inaugural de Southampton com destino a Nova 
Iorque em 10 de abril de 1912, no caminho passando em Cherbourg-Octeville, 
na França, e por Queenstown, na Irlanda. Porém, infelizmente, colidiu com um
iceberg no dia 14 de abril.

Embora houvesse algum elemento de sorte envolvido na sobrevivência, parece 
que alguns grupos de pessoas tinham mais probabilidades de sobreviver do que 
outros.

_Descubra se você sobreviveria_!
"""

with st.container():
    st.subheader('História')
    with st.expander('Resumo'):
        st.write(descricao)

## Definição dos componentes de entrada com características do passageiro
with st.container():
    st.subheader("Passageiro")
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        nome_passageiro = st.text_input(label = 'Nome:', max_chars = 10)        

    with info_col2:
        idade_passageiro = st.slider(label = 'Idade:', min_value = 0, max_value = 100)

    info_col3, info_col4, info_col5 = st.columns(3)

    with info_col3:
        sexo_passageiro = st.selectbox(label = 'Qual o sexo:', 
                                       options = ['Masculino', 'Feminino'])
    with info_col4:
        class_navio = st.selectbox(label = 'Qual a classe no navio:',
                                   options = ['1ª', '2ª', '3ª'])
    with info_col5:
        valor_passagem = st.number_input(label = 'Valor da passagem:',
                                        min_value = 0.0,
                                        max_value = 515.000,
                                        step = 1.0)

    porto_embarque = st.radio(label = 'Qual porto de embarque:',
                              options = ['Southampton', 'Cherbourg', 'Queenstown'])
    ## Necessário para ajustar orientação do componente de radio
    st.markdown("""
    <style>
        [role = 'radiogroup'] {flex-direction: row;}
        [data-baseweb] {margin-right: 1rem;}
    </style>    
    """, unsafe_allow_html = True)

    possuia_parentes = st.checkbox(label = 'Possuia parentes no navio?')
    
    qtd_irmaos_conjuge = None
    qtd_pais_filhos = None

    if possuia_parentes == True:
        detalhe_col1, detalhe_col2 = st.columns(2)
        with detalhe_col1:
            qtd_irmaos_conjuge = st.number_input(label = 'Quantidade de irmãos e/ou cônjuge:',
                                                min_value = 0,
                                                max_value = 10,
                                                step = 1)

        with detalhe_col2:
            qtd_pais_filhos = st.number_input(label = 'Quantidade de pais e/ou filhos:',
                                            min_value = 0,
                                            max_value = 10,
                                            step = 1)
## Definição do bloco para realizar o teste com base no modelo
with st.container():
    st.subheader('Teste sua sobrevivência')

    _, botao_col, _ = st.columns([2,1,2])
    with botao_col:
        bt_analisou = st.button('Analisar')

    if bt_analisou:
        with st.spinner('Lançando bote salva-vidas...'):
            time.sleep(5)
            informacoes = {
                'idade_passageiro': idade_passageiro,
                'sexo_passageiro': sexo_passageiro,
                'class_navio': class_navio,
                'valor_passagem': valor_passagem,
                'porto_embarque': porto_embarque,
                'qtd_irmaos_conjuge': qtd_irmaos_conjuge,
                'qtd_pais_filhos': qtd_pais_filhos
            }
            resultado = ModelTitanic(informacoes).predict()

            if resultado:
                st.success(f"Ufa {nome_passageiro}, você sobreviveria 😎!")
            else:
                st.info(f"Infelizmente {nome_passageiro}, você não sobreviveria 🥶!")
import streamlit as st
import requests


st.set_page_config(page_title="Mercadinho site STreamlit", page_icon="🛒")

st.title("Testando o consumo da API")

st.write("Envie os arquivos CSV para calcular possiveis promoções")

estoque = st.file_uploader("CSV de Estoque", type=["csv"])
vendas = st.file_uploader("CSV de Vendas", type=["csv"])

if st.button("Processar"):
    if estoque is None or vendas is None:
        st.error("Você precisa enviar os dois arquivos CSV.")
    else:
        with st.spinner("Processando..."):
            files = {
                "estoque_csv": ("estoque.csv", estoque.getvalue(), "text/csv"),
                "vendas_csv": ("vendas.csv", vendas.getvalue(), "text/csv"),
            }

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/pipeline-completo",
                    files=files
                )

                if response.status_code == 200:
                    resultado = response.json()
                    st.success("Processamento concluído!")
                    st.subheader("Resultado")
                    st.json(resultado)
                else:
                    st.error(f"Erro da API: {response.status_code}")
                    st.write(response.text)

            except Exception as e:
                st.error("Falha ao conectar com a API.")
                st.write(e)

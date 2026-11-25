import altair as alt
import pandas as pd
import json
import streamlit as st
from ollama import chat
from provedor_ia import (
    PROVEDOR_IA,
    MODELO_GROQ,
    obter_cliente_groq,
    verificar_groq,
    responder_groq
)
import uuid
from database import verificar_mysql
from database import (
    consultar_pedido,
    listar_pedidos,
    contar_clientes,
    analisar_pedidos,
)

from historico import (
    salvar_mensagem,
    carregar_historico,
    listar_conversas,
    excluir_conversa,
    renomear_conversa,
    exportar_conversa,
    obter_metricas,
    obter_atividade_diaria,
)

MODELO = "qwen3:4b"

def buscar_total_clientes() -> str:
    """Consulta o total de clientes cadastrados no banco de dados."""
    total = contar_clientes()
    return f"Total de clientes cadastrados: {total}"

def buscar_analise_pedidos() -> str:
    """Consulta totais de pedidos, clientes, produtos,
    status e datas de entrega. Retorna também quantidades
    agrupadas por status, produto, cliente e data."""
    resultado = analisar_pedidos()

    return json.dumps(
        resultado,
        ensure_ascii=False,
        default=str
    )


def verificar_ollama():
    try:
        import ollama

        cliente = ollama.Client(timeout=5)
        modelos = cliente.list()

        return any(
            modelo.model == MODELO
            for modelo in modelos.models
        )

    except Exception:
        return False

st.set_page_config(
    page_title="SmartAgent AI",
    page_icon="🤖",
    layout="wide"
)

INSTRUCOES = {
    "role": "system",
    "content": (
        "Você é o SmartAgent AI, um agente inteligente "
        "especializado em atendimento ao cliente e análise de dados. "
        "Responda sempre em português, de forma clara e profissional. "
        "Quando o usuário perguntar sobre um pedido específico, "
        "utilize a ferramenta buscar_pedido. "
        "Quando perguntar sobre o total de clientes, "
        "utilize a ferramenta buscar_total_clientes. "
        "Quando perguntar sobre quantidades, totais, produtos, "
        "status, cancelamentos, atrasos, entregas, datas, "
        "rankings ou comparações, utilize a ferramenta "
        "buscar_analise_pedidos. "
        "Diferencie a quantidade de registros da quantidade "
        "de valores distintos. "
        "Apresente os resultados de forma organizada. "
        "Sempre consulte as ferramentas antes de responder "
        "perguntas que dependam do banco de dados. "
        "Nunca invente informações, números ou resultados. "
        "Caso não encontre a informação, informe essa limitação. "
        "Os dados utilizados são fictícios e para demonstração. "
        "Não solicite senhas ou informações bancárias."
    )
}
if "sessao_id" not in st.session_state:
    st.session_state.sessao_id = str(uuid.uuid4())

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [INSTRUCOES.copy()]

st.title("🤖 SmartAgent AI")
st.caption(f"Agente inteligente de atendimento | Python + {PROVEDOR_IA.title()} + MySQL")

st.markdown("### 📊 Métricas de atendimento")

metricas = obter_metricas()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💬 Conversas",
    metricas["total_conversas"],
    border=True
)

col2.metric(
    "📨 Mensagens",
    metricas["total_mensagens"],
    border=True
)

col3.metric(
    "👤 Perguntas",
    metricas["total_perguntas"],
    border=True
)

col4.metric(
    "🤖 Respostas da IA",
    metricas["total_respostas"],
    border=True
)

with st.expander("📈 Atividade diária de atendimento"):
    atividade = obter_atividade_diaria()

    if atividade:
        df_atividade = pd.DataFrame(atividade)

        df_atividade["dia"] = pd.to_datetime(
            df_atividade["dia"]
        ).dt.strftime("%d/%m/%Y")

        df_atividade["perguntas"] = df_atividade["perguntas"].astype(int)
        df_atividade["respostas"] = df_atividade["respostas"].astype(int)

        dados_grafico = df_atividade.melt(
            id_vars=["dia"],
            value_vars=["perguntas", "respostas"],
            var_name="tipo",
            value_name="quantidade"
        )

        grafico = alt.Chart(dados_grafico).mark_bar(
            size=30
        ).encode(
            x=alt.X(
                "dia:N",
                title="Data",
                scale=alt.Scale(paddingInner=1),
                axis=alt.Axis(labelAngle=0)
            ),
            y=alt.Y(
                "quantidade:Q",
                title="Quantidade de mensagens"
            ),
            xOffset=alt.XOffset(
                "tipo:N",
                scale=alt.Scale(
                    domain=["perguntas", "respostas"],
                    range=[-40, 40]
                )
            ),
            color=alt.Color(
                "tipo:N",
                scale=alt.Scale(
                    domain=["perguntas", "respostas"],
                    range=["#3B82F6", "#E5B94E"]
                ),
                legend=alt.Legend(
                    title=None,
                    orient="bottom"
                )
            )
        ).properties(height=250)

        st.altair_chart(grafico, width="stretch")

    else:
        st.info("Nenhum atendimento registrado.")

with st.expander("📦 Consultar pedidos"):
    pedidos = listar_pedidos()

    if pedidos:
        df_pedidos = pd.DataFrame(pedidos)

        pesquisa = st.text_input(
            "🔎 Pesquisar pedidos",
            placeholder="Digite o número, cliente ou produto..."
        )

        if pesquisa:
            df_pedidos = df_pedidos[
                df_pedidos["id_pedido"].astype(str).str.contains(
                    pesquisa, case=False, na=False, regex=False
                )
                | df_pedidos["cliente"].str.contains(
                    pesquisa, case=False, na=False, regex=False
                )
                | df_pedidos["produto"].str.contains(
                    pesquisa, case=False, na=False, regex=False
                )
            ]


        st.dataframe(
            df_pedidos,
            width="stretch",
            hide_index=True,
            column_config={
                "id_pedido": "Nº do pedido",
                "cliente": "Cliente",
                "produto": "Produto",
                "status_pedido": "Status",
                "previsao_entrega": st.column_config.DateColumn(
                    "Previsão de entrega",
                    format="DD/MM/YYYY"
                )
            }
        )

    else:
        st.info("Nenhum pedido cadastrado.")

st.divider()
# Painel lateral do SmartAgent AI
with st.sidebar:
    st.title("🤖 SmartAgent AI")

    st.markdown("### Status do sistema")

    mysql_online = verificar_mysql()

    if PROVEDOR_IA == "groq":
        ia_online = verificar_groq()
        nome_ia = "Groq"
    else:
        ia_online = verificar_ollama()
        nome_ia = "Ollama"

    if mysql_online and ia_online:
        st.success("🟢 Agente disponível")
    else:
        st.error("🔴 Agente indisponível")

    if ia_online:
        st.caption(f"🟢 {nome_ia}: Online")
    else:
        st.caption(f"🔴 {nome_ia}: Indisponível")

    if mysql_online:
        st.caption("🟢 MySQL: Conectado")
    else:
        st.caption("🔴 MySQL: Desconectado")
    

    st.markdown("### Tecnologias")
    st.write("🐍 Python 3.12")
    if PROVEDOR_IA == "groq":
        st.write("🧠 Groq — GPT-OSS 120B")
    else:
        st.write("🧠 Ollama — Qwen3:4b")
    st.write("🗄️ MySQL")
    st.write("🌐 Streamlit")

    st.divider()

    st.markdown("### Exemplos de perguntas")
    st.info("Qual é o status do pedido 1001?")
    st.info("Quando está prevista a entrega do pedido 1003?")
    st.info("Qual produto pertence ao pedido 1004?")

    st.divider()

    
    if st.button("🗑️ Nova conversa", use_container_width=True):
        st.session_state.sessao_id = str(uuid.uuid4())
        st.session_state.mensagens = [INSTRUCOES]
        st.rerun()

    st.divider()
    st.markdown("### 🕘 Histórico de conversas")

    conversas = listar_conversas()

    if not conversas:
        st.caption("Nenhuma conversa salva.")

    
    for conversa in conversas:
        titulo = conversa["titulo"][:35]
        sessao = conversa["sessao_id"]

        if st.button(
            f"💬 {titulo}",
            key=f"conversa_{sessao}",
            use_container_width=True
        ):
            historico = carregar_historico(sessao)

            # Troca para a conversa selecionada
            st.session_state.sessao_id = sessao

            # Substitui todas as mensagens anteriores
            st.session_state.mensagens = [INSTRUCOES.copy()]

            for item in historico:
                if item["papel"] in ("user", "assistant"):
                    st.session_state.mensagens.append({
                        "role": item["papel"],
                        "content": item["mensagem"]
                    })

            st.rerun()

    st.divider()


    st.markdown("### ✏️ Renomear conversa")

    titulos = {
        conversa["sessao_id"]: conversa["titulo"]
        for conversa in conversas
    }

    if titulos:
        sessao_renomear = st.selectbox(
            "Selecione uma conversa:",
            options=list(titulos.keys()),
            format_func=lambda sessao: titulos[sessao],
            key="sessao_renomear"
        )

        novo_titulo = st.text_input(
            "Novo título da conversa:",
            max_chars=255,
            key="novo_titulo"
        )

        if st.button(
            "✏️ Renomear conversa",
            disabled=not novo_titulo.strip(),
            use_container_width=True
        ):
            renomear_conversa(
                sessao_renomear,
                novo_titulo
            )

            st.rerun()

    st.divider()


    st.markdown("### 📥 Exportar conversa")

    opcoes_exportar = {
        conversa["sessao_id"]: conversa["titulo"]
        for conversa in conversas
    }

    if opcoes_exportar:
        sessao_exportar = st.selectbox(
            "Selecione uma conversa para exportar:",
            options=list(opcoes_exportar.keys()),
            format_func=lambda sessao: opcoes_exportar[sessao],
            key="sessao_exportar"
        )

        st.download_button(
            label="📥 Baixar conversa (.txt)",
            data=exportar_conversa(sessao_exportar),
            file_name="conversa_smartagent.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()


    st.markdown("### 🗑️ Gerenciar conversas")

    opcoes = {
        conversa["sessao_id"]: conversa["titulo"]
        for conversa in conversas
    }

    if opcoes:
        sessao_excluir = st.selectbox(
            "Selecione uma conversa para excluir:",
            options=list(opcoes.keys()),
            format_func=lambda sessao: opcoes[sessao],
            key="sessao_excluir"
        )

        
        if st.session_state.pop("resetar_confirmacao", False):
            st.session_state.confirmar_exclusao = False

        confirmar = st.checkbox(
            "Confirmo que desejo excluir esta conversa.",
            key="confirmar_exclusao"
        )


        if st.button(
            "🗑️ Excluir conversa selecionada",
            disabled=not confirmar,
            use_container_width=True
        ):
            excluir_conversa(sessao_excluir)

            if st.session_state.sessao_id == sessao_excluir:
                st.session_state.sessao_id = str(uuid.uuid4())
                st.session_state.mensagens = [INSTRUCOES.copy()]

            st.session_state.resetar_confirmacao = True
            st.rerun()



def buscar_pedido(numero_pedido: int) -> str:
    """Consulta o status de um pedido pelo número."""
    pedido = consultar_pedido(numero_pedido)

    if pedido is None:
        return f"Pedido {numero_pedido} não encontrado."

    return json.dumps(pedido, ensure_ascii=False, default=str)


@st.fragment
def exibir_historico():
    with st.container(key=f"historico_{st.session_state.sessao_id}"):
        for mensagem in st.session_state.mensagens[1:]:
            if mensagem.get("role") in ("user", "assistant"):
                conteudo = mensagem.get("content")

                if conteudo:
                    with st.chat_message(mensagem["role"]):
                        st.markdown(conteudo)


exibir_historico()


pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })
    salvar_mensagem(st.session_state.sessao_id, "user", pergunta)
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando a inteligência artificial..."):
            try:
                ferramentas = {
                    "buscar_pedido": buscar_pedido,
                    "buscar_total_clientes": buscar_total_clientes,
                    "buscar_analise_pedidos": buscar_analise_pedidos
                }

                if PROVEDOR_IA == "groq":
                    texto = responder_groq(
                        st.session_state.mensagens,
                        ferramentas
                    )

                else:
                    mensagens_ollama = [
                        mensagem.copy()
                        for mensagem in st.session_state.mensagens
                    ]

                    resposta = chat(
                        model=MODELO,
                        messages=mensagens_ollama,
                        tools=list(ferramentas.values()),
                        options={"temperature": 0.2}
                    )

                    mensagens_ollama.append(
                        resposta.message.model_dump()
                    )

                    if resposta.message.tool_calls:
                        for chamada in resposta.message.tool_calls:
                            nome = chamada.function.name

                            try:
                                if nome in ferramentas:
                                    resultado = ferramentas[nome](
                                        **chamada.function.arguments
                                    )
                                else:
                                    resultado = "Ferramenta não autorizada."

                            except Exception:
                                resultado = "Não foi possível realizar a consulta."

                            mensagens_ollama.append({
                                "role": "tool",
                                "tool_name": nome,
                                "content": resultado
                            })

                        resposta = chat(
                            model=MODELO,
                            messages=mensagens_ollama,
                            options={"temperature": 0.2}
                        )

                    texto = (
                        resposta.message.content
                        or "Não foi possível gerar uma resposta."
                    )

                st.session_state.mensagens.append({
                    "role": "assistant",
                    "content": texto
                })

                salvar_mensagem(
                    st.session_state.sessao_id,
                    "assistant",
                    texto
                )

                st.markdown(texto)

            except Exception:
                st.error(
                    "Erro na comunicação com a inteligência artificial."
                )



            except Exception as erro:
                st.error(f"Erro na comunicação com o agente: {erro}")
                st.session_state.mensagens = [INSTRUCOES]

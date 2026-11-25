import os
import streamlit as st
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv
import database as db

load_dotenv()

MODO_PUBLICO = os.getenv(
    "MODO_PUBLICO", "false"
).lower() == "true"


def obter_conversas():
    if "conversas_privadas" not in st.session_state:
        st.session_state.conversas_privadas = {}

    return st.session_state.conversas_privadas


def salvar_mensagem(sessao_id, papel, mensagem):
    if not MODO_PUBLICO:
        return db.salvar_mensagem(
            sessao_id, papel, mensagem
        )

    conversas = obter_conversas()

    if sessao_id not in conversas:
        conversas[sessao_id] = {
            "titulo": None,
            "mensagens": []
        }

    conversas[sessao_id]["mensagens"].append({
        "papel": papel,
        "mensagem": mensagem,
        "data_hora": datetime.now()
    })


def carregar_historico(sessao_id):
    if not MODO_PUBLICO:
        return db.carregar_historico(sessao_id)

    conversa = obter_conversas().get(sessao_id, {})

    return conversa.get("mensagens", [])


def listar_conversas():
    if not MODO_PUBLICO:
        return db.listar_conversas()

    resultado = []

    for sessao_id, conversa in obter_conversas().items():
        mensagens = conversa["mensagens"]

        if not mensagens:
            continue

        titulo = conversa["titulo"] or next(
            (
                m["mensagem"]
                for m in mensagens
                if m["papel"] == "user"
            ),
            "Nova conversa"
        )

        resultado.append({
            "sessao_id": sessao_id,
            "titulo": titulo,
            "ultima_atividade": mensagens[-1]["data_hora"]
        })

    return sorted(
        resultado,
        key=lambda x: x["ultima_atividade"],
        reverse=True
    )


def renomear_conversa(sessao_id, novo_titulo):
    if not MODO_PUBLICO:
        return db.renomear_conversa(
            sessao_id, novo_titulo
        )

    novo_titulo = novo_titulo.strip()

    if not novo_titulo or len(novo_titulo) > 255:
        raise ValueError("Título inválido.")

    conversas = obter_conversas()

    if sessao_id in conversas:
        conversas[sessao_id]["titulo"] = novo_titulo


def excluir_conversa(sessao_id):
    if not MODO_PUBLICO:
        return db.excluir_conversa(sessao_id)

    conversa = obter_conversas().pop(sessao_id, {})

    return len(conversa.get("mensagens", []))


def exportar_conversa(sessao_id):
    if not MODO_PUBLICO:
        return db.exportar_conversa(sessao_id)

    linhas = [
        "SMARTAGENT AI",
        "Histórico de atendimento",
        "=" * 50,
        ""
    ]

    for item in carregar_historico(sessao_id):
        autor = (
            "Cliente"
            if item["papel"] == "user"
            else "SmartAgent AI"
        )

        linhas.extend([
            f"{autor}:",
            item["mensagem"],
            "",
            "-" * 50,
            ""
        ])

    return "\n".join(linhas)


def obter_metricas():
    if not MODO_PUBLICO:
        return db.obter_metricas()

    conversas = obter_conversas()

    mensagens = [
        m
        for c in conversas.values()
        for m in c["mensagens"]
    ]

    return {
        "total_conversas": sum(
            bool(c["mensagens"])
            for c in conversas.values()
        ),
        "total_mensagens": len(mensagens),
        "total_perguntas": sum(
            m["papel"] == "user"
            for m in mensagens
        ),
        "total_respostas": sum(
            m["papel"] == "assistant"
            for m in mensagens
        )
    }


def obter_atividade_diaria():
    if not MODO_PUBLICO:
        return db.obter_atividade_diaria()

    dias = defaultdict(lambda: {
        "total_mensagens": 0,
        "perguntas": 0,
        "respostas": 0
    })

    for conversa in obter_conversas().values():
        for mensagem in conversa["mensagens"]:
            dia = mensagem["data_hora"].date()

            dias[dia]["total_mensagens"] += 1

            if mensagem["papel"] == "user":
                dias[dia]["perguntas"] += 1
            else:
                dias[dia]["respostas"] += 1

    return [
        {"dia": dia, **dados}
        for dia, dados in sorted(dias.items())
    ]

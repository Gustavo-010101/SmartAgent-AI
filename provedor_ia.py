import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

PROVEDOR_IA = os.getenv("PROVEDOR_IA", "ollama").lower()

MODELO_OLLAMA = "qwen3:4b"
MODELO_GROQ = "openai/gpt-oss-120b"


def obter_cliente_groq():
    return Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )


def verificar_groq():
    try:
        cliente = obter_cliente_groq()
        modelos = cliente.models.list()

        return any(
            modelo.id == MODELO_GROQ
            for modelo in modelos.data
        )

    except Exception:
        return False

FERRAMENTAS_GROQ = [
    {
        "type": "function",
        "function": {
            "name": "buscar_pedido",
            "description": "Consulta um pedido específico pelo número.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numero_pedido": {
                        "type": "integer",
                        "description": "Número do pedido"
                    }
                },
                "required": ["numero_pedido"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_total_clientes",
            "description": "Consulta o total de clientes distintos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_analise_pedidos",
            "description": (
                "Analisa quantidades, totais, produtos, clientes, "
                "status, cancelamentos, atrasos, entregas, "
                "datas e rankings de pedidos."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]
def responder_groq(mensagens, ferramentas):
    cliente = obter_cliente_groq()

    historico = [
        {
            "role": mensagem["role"],
            "content": mensagem["content"]
        }
        for mensagem in mensagens
        if mensagem.get("role") in (
            "system", "user", "assistant"
        )
        and mensagem.get("content")
    ]

    for _ in range(5):
        resposta = cliente.chat.completions.create(
            model=MODELO_GROQ,
            messages=historico,
            tools=FERRAMENTAS_GROQ,
            tool_choice="auto",
            temperature=0.2
        )

        mensagem = resposta.choices[0].message

        print("Ferramentas solicitadas:", [
            chamada.function.name
            for chamada in (mensagem.tool_calls or [])
        ])

        if not mensagem.tool_calls:
            return (
                mensagem.content
                or "Não foi possível gerar uma resposta."
            )

        historico.append({
            "role": "assistant",
            "content": mensagem.content,
            "tool_calls": [
                chamada.model_dump()
                for chamada in mensagem.tool_calls
            ]
        })

        for chamada in mensagem.tool_calls:
            nome = chamada.function.name

            try:
                argumentos = json.loads(
                    chamada.function.arguments or "{}"
                )

                if nome in ferramentas:

                    if nome in (
                        "buscar_total_clientes",
                        "buscar_analise_pedidos"
                    ):
                        resultado = ferramentas[nome]()

                    else:
                        resultado = ferramentas[nome](
                            **argumentos
                        )

                else:
                    resultado = "Ferramenta não autorizada."


            except Exception as erro:
                print(f"Erro na ferramenta {nome}: {erro}")
                resultado = "Não foi possível realizar a consulta."

            historico.append({
                "role": "tool",
                "tool_call_id": chamada.id,
                "content": str(resultado)
            })

    return "Limite de consultas atingido. Tente novamente."

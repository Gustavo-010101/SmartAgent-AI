
import json
from ollama import chat
from database import consultar_pedido, contar_clientes, analisar_pedidos

MODELO = "qwen3:4b"


def buscar_pedido(numero_pedido: int) -> str:
    """Consulta o status de um pedido pelo número."""
    pedido = consultar_pedido(numero_pedido)

    if pedido is None:
        return f"Pedido {numero_pedido} não encontrado."

    return json.dumps(pedido, ensure_ascii=False, default=str)

def buscar_total_clientes() -> str:
    """Consulta o total de nomes distintos de clientes cadastrados."""
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


FERRAMENTAS = {
    "buscar_pedido": buscar_pedido,
    "buscar_total_clientes": buscar_total_clientes,
    "buscar_analise_pedidos": buscar_analise_pedidos
}

mensagens = [
    {
        "role": "system",
        "content": (
            "Você é o SmartAgent AI, um agente inteligente "
            "de atendimento ao cliente. "
            "Responda sempre em português. "
            "Quando o usuário perguntar sobre um pedido específico, "
            "utilize a ferramenta buscar_pedido. "
            "Quando o usuário perguntar quantos clientes existem, "
            "utilize a ferramenta buscar_total_clientes. "
            "Consulte as ferramentas disponíveis antes de responder "
            "perguntas que dependam do banco de dados. "
            "Nunca invente informações, números ou resultados. "
            "As informações consultadas são dados fictícios de teste. "
            "Não solicite senhas ou dados bancários."
        )
    }
]

print("🤖 SmartAgent AI iniciado!")
print("Digite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "sair":
        break

    if not pergunta:
        continue

    mensagens.append({
        "role": "user",
        "content": pergunta
    })

    try:
        resposta = chat(
            model=MODELO,
            messages=mensagens,
            tools=[
            buscar_pedido,
            buscar_total_clientes,
            buscar_analise_pedidos
],
            options={"temperature": 0.2}
        )

        mensagens.append(resposta.message)

        if resposta.message.tool_calls:
            for chamada in resposta.message.tool_calls:
                nome = chamada.function.name
                argumentos = chamada.function.arguments

                if nome not in FERRAMENTAS:
                    resultado = "Ferramenta não autorizada."
                else:
                    try:
                        resultado = FERRAMENTAS[nome](**argumentos)
                    except Exception as erro:
                        resultado = f"Erro na consulta: {erro}"

                mensagens.append({
                    "role": "tool",
                    "tool_name": nome,
                    "content": resultado
                })

            resposta = chat(
                model=MODELO,
                messages=mensagens,
                options={"temperature": 0.2}
            )

            mensagens.append(resposta.message)

        texto = resposta.message.content or ""
        print(f"\n🤖 SmartAgent AI: {texto}\n")

    except Exception as erro:
        print(f"\nErro: {erro}\n")
        mensagens = [mensagens[0]]

def verificar_ollama():
    try:
        import ollama

        modelos = ollama.list()

        return any(
            modelo.model == "qwen3:4b"
            for modelo in modelos.models
        )

    except Exception:
        return False


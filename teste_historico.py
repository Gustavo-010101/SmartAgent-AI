
import uuid
from database import salvar_mensagem, carregar_historico

sessao_id = str(uuid.uuid4())

salvar_mensagem(
    sessao_id,
    "user",
    "Olá, quero consultar meu pedido 1001."
)

salvar_mensagem(
    sessao_id,
    "assistant",
    "O pedido 1001 está cadastrado como Em transporte."
)

historico = carregar_historico(sessao_id)

print("Histórico recuperado do MySQL:\n")

for item in historico:
    print(f"{item['papel']}: {item['mensagem']}")

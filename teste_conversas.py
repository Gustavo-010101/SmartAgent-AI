
from database import listar_conversas

conversas = listar_conversas()

print("Conversas encontradas:\n")

for conversa in conversas:
    print("Sessão:", conversa["sessao_id"])
    print("Título:", conversa["titulo"])
    print("Última atividade:", conversa["ultima_atividade"])
    print("-" * 40)

from database import analisar_pedidos
import json

resultado = analisar_pedidos()

print("=== ANÁLISE GERAL DOS PEDIDOS ===")

print(json.dumps(
    resultado,
    indent=4,
    ensure_ascii=False,
    default=str
))
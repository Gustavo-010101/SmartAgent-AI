from database import listar_pedidos

pedidos = listar_pedidos()

print("=== PEDIDOS DO SMARTAGENT AI ===")
print(f"Total de pedidos: {len(pedidos)}")

for pedido in pedidos[:5]:
    print("------------------------------")
    print("Pedido:", pedido["id_pedido"])
    print("Cliente:", pedido["cliente"])
    print("Produto:", pedido["produto"])
    print("Status:", pedido["status_pedido"])
    print("Previsão:", pedido["previsao_entrega"])
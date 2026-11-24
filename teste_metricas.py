from database import obter_metricas

metricas = obter_metricas()

print("=== MÉTRICAS DO SMARTAGENT AI ===")
print("Total de conversas:", metricas["total_conversas"])
print("Total de mensagens:", metricas["total_mensagens"])
print("Total de perguntas:", metricas["total_perguntas"])
print("Total de respostas:", metricas["total_respostas"])
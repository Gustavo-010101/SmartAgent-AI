from database import obter_atividade_diaria

atividade = obter_atividade_diaria()

print("=== ATIVIDADE DIÁRIA DO SMARTAGENT AI ===")

for item in atividade:
    print("Data:", item["dia"])
    print("Total de mensagens:", item["total_mensagens"])
    print("Perguntas:", item["perguntas"])
    print("Respostas:", item["respostas"])
    print("-" * 40)
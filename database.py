
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar():
    provedor = os.getenv("PROVEDOR_DB", "mysql").lower()

    if provedor == "tidb":
        return mysql.connector.connect(
            host=os.getenv("TIDB_HOST"),
            port=int(os.getenv("TIDB_PORT", "4000")),
            user=os.getenv("TIDB_USER"),
            password=os.getenv("TIDB_PASSWORD"),
            database=os.getenv("TIDB_DATABASE"),
            ssl_ca=os.getenv("TIDB_SSL_CA"),
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def consultar_pedido(numero_pedido):
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id_pedido, cliente, produto,
                   status_pedido, previsao_entrega
            FROM pedidos
            WHERE id_pedido = %s
            """,
            (numero_pedido,)
        )

        pedido = cursor.fetchone()
        cursor.close()

        return pedido
    finally:
        conexao.close()


if __name__ == "__main__":
    pedido = consultar_pedido(1001)
    print(pedido)

# Salvar uma mensagem no histórico
def salvar_mensagem(sessao_id, papel, mensagem):
    if papel not in ("user", "assistant"):
        raise ValueError("Papel de mensagem inválido.")

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO historico_conversas
                (sessao_id, papel, mensagem)
            VALUES (%s, %s, %s)
            """,
            (sessao_id, papel, mensagem)
        )

        conexao.commit()
        cursor.close()

    finally:
        conexao.close()


# Recuperar mensagens de uma conversa
def carregar_historico(sessao_id):
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT papel, mensagem, data_hora
            FROM historico_conversas
            WHERE sessao_id = %s
            ORDER BY id ASC
            """,
            (sessao_id,)
        )

        mensagens = cursor.fetchall()
        cursor.close()

        return mensagens

    finally:
        conexao.close()



def listar_conversas():
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                h.sessao_id,
                COALESCE(
                    t.titulo,
                    (
                        SELECT h2.mensagem
                        FROM historico_conversas h2
                        WHERE h2.sessao_id = h.sessao_id
                        AND h2.papel = 'user'
                        ORDER BY h2.id ASC
                        LIMIT 1
                    ),
                    'Nova conversa'
                ) AS titulo,
                MAX(h.data_hora) AS ultima_atividade
            FROM historico_conversas h
            LEFT JOIN titulos_conversas t
                ON h.sessao_id = t.sessao_id
            GROUP BY h.sessao_id, t.titulo
            ORDER BY ultima_atividade DESC
        """)

        conversas = cursor.fetchall()
        cursor.close()

        return conversas

    finally:
        conexao.close()

def renomear_conversa(sessao_id, novo_titulo):
    novo_titulo = novo_titulo.strip()

    if not novo_titulo or len(novo_titulo) > 255:
        raise ValueError("O título deve ter entre 1 e 255 caracteres.")

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO titulos_conversas (sessao_id, titulo)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE titulo = %s
            """,
            (sessao_id, novo_titulo, novo_titulo)
        )

        conexao.commit()
        cursor.close()

    finally:
        conexao.close()


def excluir_conversa(sessao_id):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            """
            DELETE FROM titulos_conversas
            WHERE sessao_id = %s
            """,
            (sessao_id,)
        )

        cursor.execute(
            """
            DELETE FROM historico_conversas
            WHERE sessao_id = %s
            """,
            (sessao_id,)
        )

        quantidade = cursor.rowcount
        conexao.commit()
        cursor.close()

        return quantidade

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def exportar_conversa(sessao_id):
    historico = carregar_historico(sessao_id)

    linhas = [
        "SMARTAGENT AI",
        "Histórico de atendimento",
        "=" * 50,
        ""
    ]

    for item in historico:
        if item["papel"] == "user":
            autor = "Cliente"
        elif item["papel"] == "assistant":
            autor = "SmartAgent AI"
        else:
            continue

        linhas.append(f"{autor}:")
        linhas.append(item["mensagem"])
        linhas.append("")
        linhas.append("-" * 50)
        linhas.append("")

    return "\n".join(linhas)

def obter_metricas():
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT sessao_id) AS total_conversas,
                COUNT(*) AS total_mensagens,
                COALESCE(SUM(CASE WHEN papel = 'user'
                    THEN 1 ELSE 0 END), 0) AS total_perguntas,
                COALESCE(SUM(CASE WHEN papel = 'assistant'
                    THEN 1 ELSE 0 END), 0) AS total_respostas
            FROM historico_conversas
        """)

        return cursor.fetchone()

    finally:
        conexao.close()

def obter_atividade_diaria():
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                DATE(data_hora) AS dia,
                COUNT(*) AS total_mensagens,
                SUM(CASE WHEN papel = 'user'
                    THEN 1 ELSE 0 END) AS perguntas,
                SUM(CASE WHEN papel = 'assistant'
                    THEN 1 ELSE 0 END) AS respostas
            FROM historico_conversas
            GROUP BY DATE(data_hora)
            ORDER BY dia
        """)

        return cursor.fetchall()

    finally:
        conexao.close()

def verificar_mysql():
    conexao = None

    try:
        conexao = conectar()
        return conexao.is_connected()

    except Exception:
        return False

    finally:
        if conexao is not None:
            conexao.close()

def listar_pedidos():
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_pedido,
                cliente,
                produto,
                status_pedido,
                previsao_entrega
            FROM pedidos
            ORDER BY id_pedido
        """)

        pedidos = cursor.fetchall()

        return pedidos

    finally:
        conexao.close()

def contar_clientes():
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(DISTINCT cliente) AS total_clientes
            FROM pedidos
        """)

        resultado = cursor.fetchone()

        return resultado["total_clientes"]

    finally:
        conexao.close()

def analisar_pedidos():
    conexao = conectar()

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total_pedidos,
                COUNT(DISTINCT cliente) AS total_clientes,
                COUNT(DISTINCT produto) AS total_produtos,
                COUNT(DISTINCT status_pedido) AS total_status,
                COUNT(DISTINCT previsao_entrega) AS total_datas
            FROM pedidos
        """)

        resumo = cursor.fetchone()

        cursor.execute("""
            SELECT status_pedido, COUNT(*) AS quantidade
            FROM pedidos
            GROUP BY status_pedido
            ORDER BY quantidade DESC
        """)

        status = cursor.fetchall()

        cursor.execute("""
            SELECT produto, COUNT(*) AS quantidade
            FROM pedidos
            GROUP BY produto
            ORDER BY quantidade DESC
        """)

        produtos = cursor.fetchall()

        cursor.execute("""
            SELECT cliente, COUNT(*) AS quantidade
            FROM pedidos
            GROUP BY cliente
            ORDER BY quantidade DESC
        """)

        clientes = cursor.fetchall()

        cursor.execute("""
            SELECT previsao_entrega, COUNT(*) AS quantidade
            FROM pedidos
            GROUP BY previsao_entrega
            ORDER BY previsao_entrega
        """)

        datas = cursor.fetchall()

        return {
            "resumo": resumo,
            "pedidos_por_status": status,
            "pedidos_por_produto": produtos,
            "pedidos_por_cliente": clientes,
            "pedidos_por_data": datas
        }

    finally:
        conexao.close()
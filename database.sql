-- =============================================
-- SMARTAGENT AI
-- Script de criação do banco de dados
-- =============================================

CREATE DATABASE IF NOT EXISTS smartagent_ai
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

USE smartagent_ai;

-- Tabela de pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT NOT NULL,
    cliente VARCHAR(100) DEFAULT NULL,
    produto VARCHAR(150) DEFAULT NULL,
    status_pedido VARCHAR(50) DEFAULT NULL,
    previsao_entrega DATE DEFAULT NULL,
    PRIMARY KEY (id_pedido)
) ENGINE=InnoDB;

-- Tabela de histórico de conversas
CREATE TABLE IF NOT EXISTS historico_conversas (
    id INT NOT NULL AUTO_INCREMENT,
    sessao_id VARCHAR(36) NOT NULL,
    papel VARCHAR(20) NOT NULL,
    mensagem TEXT NOT NULL,
    data_hora TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- Tabela de títulos personalizados
CREATE TABLE IF NOT EXISTS titulos_conversas (
    sessao_id VARCHAR(36) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    PRIMARY KEY (sessao_id)
) ENGINE=InnoDB;

-- =============================================
-- Dados fictícios para demonstração
-- =============================================

INSERT IGNORE INTO pedidos (
    id_pedido,
    cliente,
    produto,
    status_pedido,
    previsao_entrega
) VALUES
    (1001, 'Ana Souza', 'Notebook', 'Em transporte', '2026-11-20'),
    (1002, 'Carlos Lima', 'Mouse Gamer', 'Entregue', '2026-11-15'),
    (1003, 'Mariana Costa', 'Teclado', 'Em preparação', '2026-11-23'),
    (1004, 'Pedro Santos', 'Monitor', 'Em transporte', '2026-11-21');

USE smartagent_ai;

INSERT IGNORE INTO pedidos (
    id_pedido,
    cliente,
    produto,
    status_pedido,
    previsao_entrega
)
WITH RECURSIVE numeros AS (
    SELECT 1005 AS n
    UNION ALL
    SELECT n + 1
    FROM numeros
    WHERE n < 1100
)
SELECT
    n,
    CONCAT(
        ELT(MOD(n, 12) + 1,
            'Lucas', 'Julia', 'Gabriel', 'Beatriz',
            'Rafael', 'Camila', 'Felipe', 'Larissa',
            'Bruno', 'Isabela', 'Matheus', 'Amanda'),
        ' ',
        ELT(MOD(FLOOR(n / 12), 8) + 1,
            'Silva', 'Santos', 'Oliveira', 'Costa',
            'Almeida', 'Pereira', 'Rodrigues', 'Ferreira')
    ),
    ELT(MOD(n, 16) + 1,
        'Notebook', 'Mouse Gamer', 'Teclado',
        'Monitor', 'Headset', 'Smartphone',
        'Tablet', 'Webcam', 'Impressora',
        'SSD 1TB', 'Memória RAM', 'Smart TV',
        'Roteador Wi-Fi', 'Placa de Vídeo',
        'Caixa de Som', 'Carregador Portátil'),
    ELT(MOD(n, 6) + 1,
        'Em preparação', 'Em transporte',
        'Entregue', 'Aguardando pagamento',
        'Cancelado', 'Atrasado'),
    DATE_ADD('2026-11-24',
        INTERVAL (MOD(n, 31) - 15) DAY)
FROM numeros;
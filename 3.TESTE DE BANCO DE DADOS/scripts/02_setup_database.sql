-- Script 02: Criação do banco de dados e tabelas base
-- Objetivo: Criar a estrutura inicial para armazenar os dados das demonstrações contábeis

CREATE DATABASE IF NOT EXISTS demonstracoes_contabeis_ans;
USE demonstracoes_contabeis_ans;

-- Tabela para armazenar os dados cadastrais das operadoras
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans CHAR(6) PRIMARY KEY,
    cnpj CHAR(14),
    razao_social VARCHAR(140),
    nome_fantasia VARCHAR(140),
    modalidade CHAR(2),
    logradouro VARCHAR(40),
    numero VARCHAR(20),
    complemento VARCHAR(40),
    bairro VARCHAR(30),
    cidade VARCHAR(30),
    uf CHAR(2),
    cep CHAR(8),
    ddd VARCHAR(4),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_de_comercializacao TINYINT,
    data_registro_ans DATE
);

-- Tabela para armazenar os dados contábeis
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    reg_ans VARCHAR(20),
    cd_conta_contabil VARCHAR(8),
    descricao VARCHAR(150),
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2),
    FOREIGN KEY (reg_ans) REFERENCES operadoras(registro_ans)
);
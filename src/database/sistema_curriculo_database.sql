-- =====================================================================
-- PERSISTÊNCIA DE DADOS — Sistema de Currículo (Aluno / FATEC-SP)
-- SGBD alvo: PostgreSQL 14+
-- Baseado no DER enviado (der_sistema_curriculo.svg)
-- =====================================================================

-- Extensão para geração de UUID nativa
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================================
-- 1. USUARIO
-- =====================================================================
CREATE TABLE usuario (
    id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome                      VARCHAR(255) NOT NULL,
    email                     VARCHAR(255) NOT NULL,
    senha_hash                VARCHAR(255) NOT NULL,
    tentativas_falhas_login   INTEGER NOT NULL DEFAULT 0,
    bloqueado_ate             TIMESTAMP,
    created_at                TIMESTAMP NOT NULL DEFAULT now(),
    updated_at                TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at                TIMESTAMP,
    CONSTRAINT uq_usuario_email UNIQUE (email)
);
CREATE INDEX idx_usuario_email ON usuario (email) WHERE deleted_at IS NULL;

-- =====================================================================
-- 2. Pool de conteúdo do usuário (reutilizável entre versões de currículo)
-- =====================================================================
CREATE TABLE formacao_academica (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id    UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    instituicao   VARCHAR(255) NOT NULL,
    curso         VARCHAR(255) NOT NULL,
    nivel         VARCHAR(100),
    data_inicio   DATE,
    data_fim      DATE,
    status        VARCHAR(50)
);
CREATE INDEX idx_formacao_usuario ON formacao_academica (usuario_id);

CREATE TABLE experiencia_profissional (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id    UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    empresa       VARCHAR(255) NOT NULL,
    cargo         VARCHAR(255) NOT NULL,
    descricao     TEXT,
    data_inicio   DATE,
    data_fim      DATE
);
CREATE INDEX idx_experiencia_usuario ON experiencia_profissional (usuario_id);

CREATE TABLE projeto_academico (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id    UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    titulo        VARCHAR(255) NOT NULL,
    descricao     TEXT,
    tecnologias   VARCHAR(255)
);
CREATE INDEX idx_projeto_usuario ON projeto_academico (usuario_id);

CREATE TABLE competencia (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id    UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    descricao     VARCHAR(255) NOT NULL,
    nivel         VARCHAR(50)
);
CREATE INDEX idx_competencia_usuario ON competencia (usuario_id);

CREATE TABLE idioma (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id    UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    idioma        VARCHAR(100) NOT NULL,
    nivel         VARCHAR(50)
);
CREATE INDEX idx_idioma_usuario ON idioma (usuario_id);

CREATE TABLE documento (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id          UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    nome_arquivo        VARCHAR(255) NOT NULL,
    tipo_arquivo        VARCHAR(100),
    url_armazenamento   TEXT NOT NULL,  -- caminho/URL no object storage (ex: S3), não o arquivo em si
    created_at          TIMESTAMP NOT NULL DEFAULT now(),
    updated_at          TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at          TIMESTAMP
);
CREATE INDEX idx_documento_usuario ON documento (usuario_id) WHERE deleted_at IS NULL;

-- =====================================================================
-- 3. CURRICULO (versões montadas pelo usuário a partir do pool acima)
-- =====================================================================
CREATE TABLE curriculo (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id    UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    titulo_versao VARCHAR(255) NOT NULL,
    layout        VARCHAR(100),
    is_public     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMP NOT NULL DEFAULT now(),
    updated_at    TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at    TIMESTAMP
);
CREATE INDEX idx_curriculo_usuario ON curriculo (usuario_id) WHERE deleted_at IS NULL;

-- =====================================================================
-- 4. Autenticação (UC02 — login / recuperar senha)
-- =====================================================================
CREATE TABLE token_reset_senha (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id  UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    token_hash  VARCHAR(255) NOT NULL,
    expira_em   TIMESTAMP NOT NULL,
    usado_em    TIMESTAMP,
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX idx_token_reset_usuario ON token_reset_senha (usuario_id);
CREATE UNIQUE INDEX uq_token_reset_hash ON token_reset_senha (token_hash);

CREATE TABLE sessao (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id    UUID NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    criada_em     TIMESTAMP NOT NULL DEFAULT now(),
    expira_em     TIMESTAMP NOT NULL,
    revogada_em   TIMESTAMP
);
CREATE INDEX idx_sessao_usuario ON sessao (usuario_id);

-- =====================================================================
-- 5. Tabelas de junção — cada versão de currículo escolhe itens do pool
-- =====================================================================
CREATE TABLE curriculo_formacao (
    curriculo_id UUID NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    formacao_id  UUID NOT NULL REFERENCES formacao_academica(id) ON DELETE CASCADE,
    PRIMARY KEY (curriculo_id, formacao_id)
);

CREATE TABLE curriculo_experiencia (
    curriculo_id    UUID NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    experiencia_id  UUID NOT NULL REFERENCES experiencia_profissional(id) ON DELETE CASCADE,
    PRIMARY KEY (curriculo_id, experiencia_id)
);

CREATE TABLE curriculo_projeto (
    curriculo_id UUID NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    projeto_id   UUID NOT NULL REFERENCES projeto_academico(id) ON DELETE CASCADE,
    PRIMARY KEY (curriculo_id, projeto_id)
);

CREATE TABLE curriculo_competencia (
    curriculo_id    UUID NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    competencia_id  UUID NOT NULL REFERENCES competencia(id) ON DELETE CASCADE,
    PRIMARY KEY (curriculo_id, competencia_id)
);

CREATE TABLE curriculo_idioma (
    curriculo_id UUID NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    idioma_id    UUID NOT NULL REFERENCES idioma(id) ON DELETE CASCADE,
    PRIMARY KEY (curriculo_id, idioma_id)
);

CREATE TABLE curriculo_documento (
    curriculo_id  UUID NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    documento_id  UUID NOT NULL REFERENCES documento(id) ON DELETE CASCADE,
    PRIMARY KEY (curriculo_id, documento_id)
);

-- =====================================================================
-- 6. Exportação e integração (UC07/UC08/UC09)
-- =====================================================================
CREATE TABLE exportacao (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    curriculo_id     UUID NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    formato          VARCHAR(20) NOT NULL CHECK (formato IN ('PDF', 'DOCX', 'JSON')),
    data_exportacao  TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX idx_exportacao_curriculo ON exportacao (curriculo_id);

CREATE TABLE sistema_externo (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome           VARCHAR(255) NOT NULL,
    token_acesso   VARCHAR(255) NOT NULL,
    url_endpoint   VARCHAR(500) NOT NULL
);

CREATE TABLE integracao_log (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sistema_externo_id    UUID NOT NULL REFERENCES sistema_externo(id) ON DELETE CASCADE,
    curriculo_id          UUID REFERENCES curriculo(id) ON DELETE SET NULL,
    tipo_operacao         VARCHAR(50) NOT NULL,
    status                VARCHAR(50) NOT NULL,
    data_hora             TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX idx_integracao_sistema ON integracao_log (sistema_externo_id);
CREATE INDEX idx_integracao_curriculo ON integracao_log (curriculo_id);

-- =====================================================================
-- Fim do script
-- =====================================================================
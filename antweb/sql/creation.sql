CREATE TABLE perfil (
    id        INTEGER       PRIMARY KEY
                            UNIQUE
                            NOT NULL,
    nome      VARCHAR (32)  UNIQUE
                            NOT NULL,
    descricao VARCHAR (250) 
);

CREATE TABLE usuario (
    id            INTEGER       PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    nome          VARCHAR (16)  NOT NULL,
    nome_completo VARCHAR (120) 
);

CREATE TABLE acao (
    id        INTEGER       PRIMARY KEY
                            UNIQUE
                            NOT NULL,
    descricao VARCHAR (128) NOT NULL
                            UNIQUE,
    grupo     VARCHAR (32)  NOT NULL
                            DEFAULT (0) 
);

CREATE TABLE perfil_acao (
    id_perfil INTEGER REFERENCES perfil (id),
    id_acao   INTEGER REFERENCES acao (id),
    PRIMARY KEY (
        id_perfil,
        id_acao
    )
);

CREATE TABLE usuario_acao (
    id_usuario INTEGER REFERENCES usuario (id),
    id_acao    INTEGER REFERENCES acao (id),
    PRIMARY KEY (
        id_usuario,
        id_acao
    )
);

INSERT INTO perfil
    ( id, nome,            descricao                                                       )
    VALUES
    (  1, 'Administrador', 'Usuário com permissão para executar todas as ações do sistema' );

INSERT INTO acao
    (    id, descricao,                             grupo      )
    VALUES
    (     1, 'Consultar dados de usuários',         'Básico'   ),
    (     2, 'Consultar permissões de usuários',    'Básico'   ),
    (     3, 'Editar os próprios dados de usuário', 'Básico'   ),
    (  1001, 'Incluir usuário',                     'Gerência' ),
    (  1002, 'Editar dados de usuários',            'Gerência' ),
    (  1003, 'Editar permissões de usuários',       'Gerência' );

INSERT INTO perfil_acao
    ( id_acao, id_perfil )
    VALUES 
    (       1,         1 ),
    (       2,         1 ),
    (       3,         1 ),
    (    1001,         1 ),
    (    1002,         1 ),
    (    1003,         1 );

COMMIT;
INSERT INTO tb_tipo_de_usuario(
            id_tipo_de_usuario, descricao)
    VALUES (1, 'Sistema');

INSERT INTO tb_tipo_de_usuario(
            id_tipo_de_usuario, descricao)
    VALUES (2, 'Contato');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (1, 'Disponível');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (2, 'Bloqueado');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (3, 'Aprovado');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (4, 'Reprovado');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (5, 'Exlcuído');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (6, 'Obsoleto');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (7, 'Pendente');

INSERT INTO tb_estado_da_versao(
            id_estado_da_versao, descricao)
    VALUES (8, 'Vencido');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (1, 'Check-in');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (2, 'Check-out');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (3, 'Aprovar');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (4, 'Reprovar');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (5, 'Exlcuir');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (6, 'Download');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (7, 'Visualizar');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (8, 'Encaminhar');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (9, 'Obsoletar');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (10, 'Enviar por Email');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (11, 'Publicar');

INSERT INTO tb_tipo_de_evento(
            id_tipo_evento, descricao)
    VALUES (12, 'Login');

INSERT INTO tb_tipo_de_indice(
            id_tipo_indice, descricao)
    VALUES (1, 'String');

INSERT INTO auth_group(
            id, name)
    VALUES (1, 'Administradores');

INSERT INTO auth_group(
            id, name)
    VALUES (2, 'Usuários');

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (1, 1, 32);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (2, 1, 33);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (3, 1, 55);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (4, 1, 24);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (5, 1, 22);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (6, 1, 23);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (7, 1, 56);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (8, 1, 57);

INSERT INTO auth_group_permissions(
            id, group_id, permission_id)
    VALUES (9, 1, 31);

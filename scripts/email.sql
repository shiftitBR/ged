INSERT INTO tb_tipo_de_email(
            id_tipo_email, descricao)
    VALUES (1, 'Pendência Recebida');

INSERT INTO tb_tipo_de_email(
            id_tipo_email, descricao)
    VALUES (2, 'Pendência Aprovada');

INSERT INTO tb_tipo_de_email(
            id_tipo_email, descricao)
    VALUES (3, 'Pendência Reprovada');

INSERT INTO tb_tipo_de_email(
            id_tipo_email, descricao)
    VALUES (4, 'Documento Vencendo');

INSERT INTO tb_tipo_de_email(
            id_tipo_email, descricao)
    VALUES (5, 'Pendência Assinada');

INSERT INTO tb_email(
            id_email, tipo_email_id, titulo, mensagem)
    VALUES (1, 1, 'Pendência Recebida', 'Você Recebeu uma nova pendência!');

INSERT INTO tb_email(
            id_email, tipo_email_id, titulo, mensagem)
    VALUES (2, 2, 'Pendência Aprovada', 'Uma pendência sua foi Aprovada!');

INSERT INTO tb_email(
            id_email, tipo_email_id, titulo, mensagem)
    VALUES (3, 3, 'Pendência Reprovada', 'Uma pendência sua foi Reprovada!');

INSERT INTO tb_email(
            id_email, tipo_email_id, titulo, mensagem)
    VALUES (4, 4, 'Documento Vencendo', 'Você tem um documento com vencimento para os próximos 5 dias!');

INSERT INTO tb_email(
            id_email, tipo_email_id, titulo, mensagem)
    VALUES (5, 5, 'Pendência Assinada', 'Uma pendência sua foi Assinada!');

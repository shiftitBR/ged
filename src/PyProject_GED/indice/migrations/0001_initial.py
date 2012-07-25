# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tipo_de_Indice'
        db.create_table('tb_tipo_de_indice', (
            ('id_tipo_indice', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['autenticacao.Empresa'])),
        ))
        db.send_create_signal('indice', ['Tipo_de_Indice'])

        # Adding model 'Indice'
        db.create_table('tb_indice', (
            ('id_indice', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('tipo_indice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indice.Tipo_de_Indice'])),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['autenticacao.Empresa'])),
        ))
        db.send_create_signal('indice', ['Indice'])

        # Adding model 'Indice_Versao_Valor'
        db.create_table('tb_indice_versao_valor', (
            ('id_indice_versao_valor', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('indice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indice.Indice'])),
            ('versao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documento.Versao'])),
            ('valor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['autenticacao.Empresa'])),
        ))
        db.send_create_signal('indice', ['Indice_Versao_Valor'])


    def backwards(self, orm):
        # Deleting model 'Tipo_de_Indice'
        db.delete_table('tb_tipo_de_indice')

        # Deleting model 'Indice'
        db.delete_table('tb_indice')

        # Deleting model 'Indice_Versao_Valor'
        db.delete_table('tb_indice_versao_valor')


    models = {
        'autenticacao.empresa': {
            'Meta': {'object_name': 'Empresa', 'db_table': "'tb_empresa'"},
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'banco': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'complemento': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'ddd': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'eh_ativo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id_empresa': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'pasta_raiz': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'rua': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'uf': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'autenticacao.tipo_de_usuario': {
            'Meta': {'object_name': 'Tipo_de_Usuario', 'db_table': "'tb_tipo_de_usuario'"},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_tipo_usuario': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'autenticacao.usuario': {
            'Meta': {'object_name': 'Usuario', 'db_table': "'tb_usuario'", '_ormbases': ['auth.User']},
            'eh_ativo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'tipo_usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Tipo_de_Usuario']"}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'documento.documento': {
            'Meta': {'object_name': 'Documento', 'db_table': "'tb_documento'"},
            'assunto': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'data_descarte': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'data_validade': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'eh_publico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_documento': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'primary_key': 'True'}),
            'pasta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Pasta']"}),
            'tipo_documento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documento.Tipo_de_Documento']"}),
            'usr_responsavel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Usuario']"}),
            'versao_atual': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        'documento.estado_da_versao': {
            'Meta': {'object_name': 'Estado_da_Versao', 'db_table': "'tb_estado_da_versao'"},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id_estado_da_versao': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'documento.tipo_de_documento': {
            'Meta': {'object_name': 'Tipo_de_Documento', 'db_table': "'tb_tipo_de_documento'"},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eh_nativo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_tipo_documento': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'documento.versao': {
            'Meta': {'object_name': 'Versao', 'db_table': "'tb_versao'"},
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {}),
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documento.Documento']"}),
            'dsc_modificacao': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'eh_assinado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documento.Estado_da_Versao']"}),
            'id_versao': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'primary_key': 'True'}),
            'protocolo': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multiuploader.MultiuploaderImage']"}),
            'usr_criador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Usuario']"}),
            'versao': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        'indice.indice': {
            'Meta': {'object_name': 'Indice', 'db_table': "'tb_indice'"},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_indice': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'tipo_indice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indice.Tipo_de_Indice']"})
        },
        'indice.indice_versao_valor': {
            'Meta': {'object_name': 'Indice_Versao_Valor', 'db_table': "'tb_indice_versao_valor'"},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_indice_versao_valor': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'indice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indice.Indice']"}),
            'valor': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'versao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documento.Versao']"})
        },
        'indice.tipo_de_indice': {
            'Meta': {'object_name': 'Tipo_de_Indice', 'db_table': "'tb_tipo_de_indice'"},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_tipo_indice': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'multiuploader.multiuploaderimage': {
            'Meta': {'object_name': 'MultiuploaderImage'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            'key_data': ('django.db.models.fields.CharField', [], {'max_length': '90', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'seguranca.pasta': {
            'Meta': {'object_name': 'Pasta', 'db_table': "'tb_pasta'"},
            'diretorio': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_pasta': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pasta_pai': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Pasta']", 'null': 'True'})
        }
    }

    complete_apps = ['indice']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tipo_de_Documento'
        db.create_table('tb_tipo_de_documento', (
            ('id_tipo_documento', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('eh_nativo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('documento', ['Tipo_de_Documento'])

        # Adding model 'Documento'
        db.create_table('tb_documento', (
            ('id_documento', self.gf('django.db.models.fields.IntegerField')(max_length=10, primary_key=True)),
            ('tipo_documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documento.Tipo_de_Documento'])),
            ('usr_responsavel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['autenticacao.Usuario'])),
            ('pasta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Pasta'])),
            ('assunto', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('versao_atual', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('data_validade', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_descarte', self.gf('django.db.models.fields.DateTimeField')()),
            ('eh_pulbico', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('documento', ['Documento'])

        # Adding model 'Estado_da_Versao'
        db.create_table('tb_estado_da_versao', (
            ('id_estado_da_versao', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('documento', ['Estado_da_Versao'])

        # Adding model 'Versao'
        db.create_table('tb_versao', (
            ('id_versao', self.gf('django.db.models.fields.IntegerField')(max_length=10, primary_key=True)),
            ('documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documento.Documento'])),
            ('usr_criador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['autenticacao.Usuario'])),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['documento.Estado_da_Versao'])),
            ('versao', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('dsc_modificacao', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('arquivo', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('protocolo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')()),
            ('eh_assinado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('documento', ['Versao'])


    def backwards(self, orm):
        # Deleting model 'Tipo_de_Documento'
        db.delete_table('tb_tipo_de_documento')

        # Deleting model 'Documento'
        db.delete_table('tb_documento')

        # Deleting model 'Estado_da_Versao'
        db.delete_table('tb_estado_da_versao')

        # Deleting model 'Versao'
        db.delete_table('tb_versao')


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
            'data_descarte': ('django.db.models.fields.DateTimeField', [], {}),
            'data_validade': ('django.db.models.fields.DateTimeField', [], {}),
            'eh_pulbico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'id_tipo_documento': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'documento.versao': {
            'Meta': {'object_name': 'Versao', 'db_table': "'tb_versao'"},
            'arquivo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {}),
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documento.Documento']"}),
            'dsc_modificacao': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'eh_assinado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['documento.Estado_da_Versao']"}),
            'id_versao': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'primary_key': 'True'}),
            'protocolo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'usr_criador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Usuario']"}),
            'versao': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        'seguranca.pasta': {
            'Meta': {'object_name': 'Pasta', 'db_table': "'tb_pasta'"},
            'diretorio': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id_pasta': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pasta_pai': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Pasta']"})
        }
    }

    complete_apps = ['documento']
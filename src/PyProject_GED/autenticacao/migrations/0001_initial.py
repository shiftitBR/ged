# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Empresa'
        db.create_table('tb_empresa', (
            ('id_empresa', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cnpj', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('ddd', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('telefone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('cep', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('rua', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('complemento', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('bairro', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('cidade', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('uf', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('banco', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('eh_ativo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('autenticacao', ['Empresa'])

        # Adding model 'Tipo_de_Usuario'
        db.create_table('tb_tipo_de_usuario', (
            ('id_tipo_usuario', self.gf('django.db.models.fields.IntegerField')(max_length=2, primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('autenticacao', ['Tipo_de_Usuario'])

        # Adding model 'Usuario'
        db.create_table('tb_usuario', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['autenticacao.Empresa'])),
            ('tipo_usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['autenticacao.Tipo_de_Usuario'])),
            ('eh_ativo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('autenticacao', ['Usuario'])


    def backwards(self, orm):
        # Deleting model 'Empresa'
        db.delete_table('tb_empresa')

        # Deleting model 'Tipo_de_Usuario'
        db.delete_table('tb_tipo_de_usuario')

        # Deleting model 'Usuario'
        db.delete_table('tb_usuario')


    models = {
        'autenticacao.empresa': {
            'Meta': {'object_name': 'Empresa', 'db_table': "'tb_empresa'"},
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'banco': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'complemento': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'ddd': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'eh_ativo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id_empresa': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'rua': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'uf': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'})
        },
        'autenticacao.tipo_de_usuario': {
            'Meta': {'object_name': 'Tipo_de_Usuario', 'db_table': "'tb_tipo_de_usuario'"},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id_tipo_usuario': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'primary_key': 'True'})
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
        }
    }

    complete_apps = ['autenticacao']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pasta'
        db.create_table('tb_pasta', (
            ('id_pasta', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('pasta_pai', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Pasta'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('diretorio', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('seguranca', ['Pasta'])

        # Adding model 'Grupo'
        db.create_table('tb_grupo', (
            ('id_grupo', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('descricacao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('seguranca', ['Grupo'])

        # Adding model 'Grupo_Pasta'
        db.create_table('tb_grupo_pasta', (
            ('id_grupo_pasta', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Grupo'])),
            ('pasta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Pasta'])),
        ))
        db.send_create_signal('seguranca', ['Grupo_Pasta'])

        # Adding model 'Funcao'
        db.create_table('tb_funcao', (
            ('id_funcao', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('descricacao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('seguranca', ['Funcao'])

        # Adding model 'Funcao_Grupo'
        db.create_table('tb_funcao_grupo', (
            ('id_funcao_grupo', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('funcao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Funcao'])),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Grupo'])),
        ))
        db.send_create_signal('seguranca', ['Funcao_Grupo'])

        # Adding model 'Firewall'
        db.create_table('tb_firewall', (
            ('id_firewall', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descricacao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('seguranca', ['Firewall'])

        # Adding model 'Firewall_Grupo'
        db.create_table('tb_firewall_grupo', (
            ('id_firewall_grupo', self.gf('django.db.models.fields.IntegerField')(max_length=3, primary_key=True)),
            ('firewall', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Funcao'])),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Grupo'])),
        ))
        db.send_create_signal('seguranca', ['Firewall_Grupo'])


    def backwards(self, orm):
        # Deleting model 'Pasta'
        db.delete_table('tb_pasta')

        # Deleting model 'Grupo'
        db.delete_table('tb_grupo')

        # Deleting model 'Grupo_Pasta'
        db.delete_table('tb_grupo_pasta')

        # Deleting model 'Funcao'
        db.delete_table('tb_funcao')

        # Deleting model 'Funcao_Grupo'
        db.delete_table('tb_funcao_grupo')

        # Deleting model 'Firewall'
        db.delete_table('tb_firewall')

        # Deleting model 'Firewall_Grupo'
        db.delete_table('tb_firewall_grupo')


    models = {
        'seguranca.firewall': {
            'Meta': {'object_name': 'Firewall', 'db_table': "'tb_firewall'"},
            'descricacao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id_firewall': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'seguranca.firewall_grupo': {
            'Meta': {'object_name': 'Firewall_Grupo', 'db_table': "'tb_firewall_grupo'"},
            'firewall': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Funcao']"}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Grupo']"}),
            'id_firewall_grupo': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'seguranca.funcao': {
            'Meta': {'object_name': 'Funcao', 'db_table': "'tb_funcao'"},
            'descricacao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id_funcao': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'seguranca.funcao_grupo': {
            'Meta': {'object_name': 'Funcao_Grupo', 'db_table': "'tb_funcao_grupo'"},
            'funcao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Funcao']"}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Grupo']"}),
            'id_funcao_grupo': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        'seguranca.grupo': {
            'Meta': {'object_name': 'Grupo', 'db_table': "'tb_grupo'"},
            'descricacao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id_grupo': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'seguranca.grupo_pasta': {
            'Meta': {'object_name': 'Grupo_Pasta', 'db_table': "'tb_grupo_pasta'"},
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Grupo']"}),
            'id_grupo_pasta': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'pasta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Pasta']"})
        },
        'seguranca.pasta': {
            'Meta': {'object_name': 'Pasta', 'db_table': "'tb_pasta'"},
            'diretorio': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id_pasta': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pasta_pai': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Pasta']"})
        }
    }

    complete_apps = ['seguranca']
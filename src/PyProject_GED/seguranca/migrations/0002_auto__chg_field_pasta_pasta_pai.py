# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Pasta.pasta_pai'
        db.alter_column('tb_pasta', 'pasta_pai_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seguranca.Pasta'], null=True))

    def backwards(self, orm):

        # Changing field 'Pasta.pasta_pai'
        db.alter_column('tb_pasta', 'pasta_pai_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['seguranca.Pasta']))

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
            'pasta_pai': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Pasta']", 'null': 'True'})
        }
    }

    complete_apps = ['seguranca']
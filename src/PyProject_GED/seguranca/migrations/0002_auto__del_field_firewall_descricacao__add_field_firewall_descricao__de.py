# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Firewall.descricacao'
        db.delete_column('tb_firewall', 'descricacao')

        # Adding field 'Firewall.descricao'
        db.add_column('tb_firewall', 'descricao',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Deleting field 'Funcao.descricacao'
        db.delete_column('tb_funcao', 'descricacao')

        # Adding field 'Funcao.descricao'
        db.add_column('tb_funcao', 'descricao',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Deleting field 'Grupo.descricacao'
        db.delete_column('tb_grupo', 'descricacao')

        # Adding field 'Grupo.descricao'
        db.add_column('tb_grupo', 'descricao',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Firewall.descricacao'
        db.add_column('tb_firewall', 'descricacao',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Deleting field 'Firewall.descricao'
        db.delete_column('tb_firewall', 'descricao')

        # Adding field 'Funcao.descricacao'
        db.add_column('tb_funcao', 'descricacao',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Deleting field 'Funcao.descricao'
        db.delete_column('tb_funcao', 'descricao')

        # Adding field 'Grupo.descricacao'
        db.add_column('tb_grupo', 'descricacao',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Deleting field 'Grupo.descricao'
        db.delete_column('tb_grupo', 'descricao')


    models = {
        'autenticacao.empresa': {
            'Meta': {'object_name': 'Empresa', 'db_table': "'tb_empresa'"},
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
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
        'seguranca.firewall': {
            'Meta': {'object_name': 'Firewall', 'db_table': "'tb_firewall'"},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
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
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
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
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'id_grupo': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'seguranca.grupo_pasta': {
            'Meta': {'object_name': 'Grupo_Pasta', 'db_table': "'tb_grupo_pasta'"},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autenticacao.Empresa']"}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Grupo']"}),
            'id_grupo_pasta': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'primary_key': 'True'}),
            'pasta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seguranca.Pasta']"})
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

    complete_apps = ['seguranca']
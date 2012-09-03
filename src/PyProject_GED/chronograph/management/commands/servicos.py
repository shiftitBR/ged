'''
Created on May 22, 2012

@author: spengler
'''

from django.core.management.base import BaseCommand, CommandError

import constantes #@UnresolvedImport
import os


class Command(BaseCommand):
    args = '<vLinhaDeComando vLinhaDeComando...>'
    help = 'Executa Servicos'

    def handle(self, *args, **options):
        iCodigoServico= 1
        self.stdout.write('iCodigoServico')
        self.stdout.write('iIDEmpresa') 
        try:
            #if int(iCodigoServico) == constantes.cntServicosEnviaAlertaPendencia:
            self.stdout.write('Servico "%s" iniciado!\n' % iCodigoServico)
            os.system('mkdir /home/spengler/ged_documentos/teste1')
            self.stdout.write('>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.stdout.write('envia alerta')
            self.stdout.write('Servico "%s" finalizado!\n' % iCodigoServico)
        except Exception, e:
            print 'Nao foi possivel executar o sevico: ' + str(e)
            raise CommandError('Servico "%s" nao foi executado!' % iCodigoServico)
            

        self.stdout.write('Servico "%s" executado com sucesso!\n' % iCodigoServico)
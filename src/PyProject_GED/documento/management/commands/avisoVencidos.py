'''
Created on May 22, 2012

@author: spengler
'''

from django.core.management.base    import CommandError
from django.core.management.base import NoArgsCommand
from PyProject_GED.documento.models import Documento


class Command(NoArgsCommand):
    help = 'Executa Servicos'

    def handle_noargs(self, *args, **options):
        iNomeServico= 'AvisoVencidos'
        try:
            self.stdout.write('Servico "%s" iniciado!\n' % iNomeServico)
            Documento().notificaUsuarioResponsavelPorDocumentosVencendo()
            self.stdout.write('Servico "%s" finalizado!\n' % iNomeServico)
        except Exception, e:
            print 'Nao foi possivel executar o sevico: ' + str(e)
            raise CommandError('Servico "%s" nao foi executado!' % iNomeServico)
            

        self.stdout.write('Servico "%s" executado com sucesso!\n' % iNomeServico)
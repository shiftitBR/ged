'''
Created on May 22, 2012

@author: spengler
'''

from django.core.management.base    import CommandError
from django.core.management.base import NoArgsCommand
import os


class Command(NoArgsCommand):
    help = 'Executa Servicos'

    def handle_noargs(self, *args, **options):
        iNomeServico= 'LibreOffice'
        try:            
            self.stdout.write('Servico "%s" iniciado!\n' % iNomeServico)
            os.system('unset DISPLAY')
            os.system('libreoffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" --nologo --headless --invisible --nofirststartwizard')
            self.stdout.write('Servico "%s" finalizado!\n' % iNomeServico)
        except Exception, e:
            print 'Nao foi possivel executar o sevico: ' + str(e)
            raise CommandError('Servico "%s" nao foi executado!' % iNomeServico)
            

        self.stdout.write('Servico "%s" executado com sucesso!\n' % iNomeServico)
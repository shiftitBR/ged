'''
Created on May 22, 2012

@author: spengler
'''

from django.core.management.base import BaseCommand, CommandError
from PyProject_GED.autenticacao.models          import Empresa
from PyProject_GED.autenticacao.models          import Tipo_de_Usuario
from PyProject_GED.seguranca.models             import Pasta
from PyProject_GED.documento.models             import Tipo_de_Documento
from PyProject_GED.indice.models                import Tipo_de_Indice
from PyProject_GED                              import oControle  

import constantes #@UnresolvedImport


class Command(BaseCommand):
    args = '<vLinhaDeComando vLinhaDeComando...>'
    help = 'Executa Servicos'

    def handle(self, *args, **options):
        iCodigoServico, iIDEmpresa, iAliasBanco= args
        oControle.setBanco(iAliasBanco)
        iDiretorioArquivos= '/home/shift/webapps/ged/PyProject_GED/media/documentos//shift_ged_empresa_%03d'
        try:
            if int(iCodigoServico) == constantes.cntServicosCriaEmpresa:
                self.stdout.write('Servico "%s" iniciado!\n' % iCodigoServico)
                iEmpresa= Empresa.objects.using(constantes.cntConfiguracaoBancoPadrao).filter(id_empresa=iIDEmpresa)[0]
                iEmpresa.save(False)
                self.stdout.write('Servico "%s" finalizado!\n' % iCodigoServico)
            elif int(iCodigoServico) == constantes.cntServicosCriaTipoUsuario:
                self.stdout.write('Servico "%s" iniciado!\n' % iCodigoServico)
                iTipoUsuario= Tipo_de_Usuario()
                iTipoUsuario.id_tipo_usuario= 1
                iTipoUsuario.descricao= 'Administrador'
                iTipoUsuario.save()
                self.stdout.write('Servico "%s" finalizado!\n' % iCodigoServico)
            elif int(iCodigoServico) == constantes.cntServicosCriaPastas:
                self.stdout.write('Servico "%s" iniciado!\n' % iCodigoServico)
                iPastaRaiz= Pasta()
                iPastaRaiz.nome= 'Pasta Raiz'
                iPastaRaiz.diretorio= '%s/1' % iDiretorioArquivos
                iPastaRaiz.save()
                iPastaModelo= Pasta()
                iPastaModelo.nome= 'Modelos'
                iPastaModelo.diretorio= '%s/1/2' % iDiretorioArquivos
                self.stdout.write('Servico "%s" finalizado!\n' % iCodigoServico)
            elif int(iCodigoServico) == constantes.cntServicosCriaTipoDeIndice:
                self.stdout.write('Servico "%s" iniciado!\n' % iCodigoServico)
                iTipoDeIndice= Tipo_de_Indice()
                iTipoDeIndice.descricao= 'String'
                iTipoDeIndice.save()
                self.stdout.write('Servico "%s" finalizado!\n' % iCodigoServico)
            elif int(iCodigoServico) == constantes.cntServicosCriaTipodeDocumento:
                self.stdout.write('Servico "%s" iniciado!\n' % iCodigoServico)
                iTipoDeDocumento= Tipo_de_Documento()
                iTipoDeDocumento.descricao= 'Modelo'
                iTipoDeDocumento.eh_nativo= True
                iTipoDeDocumento.save()
                self.stdout.write('Servico "%s" finalizado!\n' % iCodigoServico)
        except Exception, e:
            print 'Nao foi possivel executar o sevico: ' + str(e)
            raise CommandError('Servico "%s" nao foi executado!' % iCodigoServico)
            

        self.stdout.write('Servico "%s" executado com sucesso!\n' % iCodigoServico)
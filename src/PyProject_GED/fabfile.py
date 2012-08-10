from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

import datetime
import xmlrpclib

env.hosts = ['shift@shift.webfactional.com']


def roda_teste():
    with settings(warn_only=True):
        result1 = local('python ./manage.py test autenticacao', capture=True)
        result2 = local('python ./manage.py test documento', capture=True)
        result3 = local('python ./manage.py test historico', capture=True)
        result4 = local('python ./manage.py test indice', capture=True)
        result5 = local('python ./manage.py test seguranca', capture=True)
        result6 = local('python ./manage.py test ocr', capture=True)
        
    if (result1.failed or result2.failed or result3.failed  or result4.failed  or result5.failed or result6.failed) and not confirm("O teste FALHOU! Continuar mesmo assim?"):
        abort("Abortando...")

def roda_teste_remoto(vDiretorio):
    with settings(warn_only=True):
        with cd(vDiretorio):
            result = run('python2.7 ./manage.py test cadastro')
    if result.failed and not confirm("O teste FALHOU! Continuar mesmo assim?"):
        abort("Abortando...")

def fazer_commit():
    local("git add -p && git commit")

def fazer_push():
    local("git push -u origin master")
    
def cria_tag_master(vNomeTag):
    if vNomeTag == None:
        iNomeTag= 'Producao_%s_%s' % (str(datetime.datetime.today().year), str(datetime.datetime.today().timetuple()[7]))
    else:
        iNomeTag= vNomeTag
    local("git tag %s HEAD" % iNomeTag)

def cria_tag_producao(vNomeTag):
    if vNomeTag == None:
        iNomeTag= 'Deploy_%s_%s' % (str(datetime.datetime.today().year), str(datetime.datetime.today().timetuple()[7]))
    else:
        iNomeTag= vNomeTag
    local("git tag %s HEAD" % iNomeTag)

def push_tag():
    local('git push --tags')

def cria_branch():
    try:
        local('git branch -d producao')
    except:
        pass
    local("git branch producao master")
    
def push_producao():
    local('git push -u origin producao')
    
def checkout(vBranch):
    local('git checkout %s' % vBranch)
    
def pull():
    local('git pull')

def fetch_pull_remoto(vDiretorio):
    with cd(vDiretorio):
        run('git fetch')
        run('git pull')

def clone_producao(vDiretorio):
    try:
        run('rm -r -I %s' % vDiretorio)
        run('mkdir %s' % vDiretorio)
    except:
        pass
    run("git clone https://shiftitBR@github.com/shiftitBR/ged.git %s" % vDiretorio)

def checkout_remoto(vDiretorio):
    with cd(vDiretorio):
        run('git checkout producao')

def sincronizaBanco_remoto(vDiretorio):
    with cd(vDiretorio):
        run('python2.7 %s%s syncdb' % (vDiretorio, 'manage.py'))

def sincronizaBanco_local(vDiretorio, vDataBase):
    with cd(vDiretorio):
        local('python2.7 %s%s syncdb --database="%s" --noinput' % (vDiretorio, '/manage.py', vDataBase))

def migraBanco_local(vDiretorio, vDataBase):
    with cd(vDiretorio):
        iAplicacao= ''
        local('python2.7 %s%s migrate %s --database="%s"' % (vDiretorio, '/manage.py', iAplicacao , vDataBase))

def reiniciaApache_remoto(vDiretorio):
    with cd(vDiretorio):
        run('./restart')

def reiniciaApache_local(vDiretorio):
    local('%s./restart' % vDiretorio)

def cria_pastaLog(vDiretorio):
    with cd(vDiretorio):
        run('mkdir %s%s' % (vDiretorio, 'log/')) 

def cria_pasta(vDiretorio, vAlias, vIDPastaRaiz, vIDPastaModelo):
    with cd(vDiretorio):
        local('mkdir %s%s' % (vDiretorio, vAlias)) 
        local('mkdir %s%s/%s' % (vDiretorio, vAlias, vIDPastaRaiz)) 
        local('mkdir %s%s/%s/%s' % (vDiretorio, 
                                    vAlias, 
                                    str(vIDPastaRaiz), 
                                    str(vIDPastaModelo)))
        
def copia_settingsLocal(vDiretorioArquivos, vDiretorioApp):
    with cd(vDiretorioArquivos):
        run('cp %s%s %s%s' % (vDiretorioArquivos, 'local_settings.py', vDiretorioApp, 'local_settings.py'))

def merge_branch():
    local('git checkout master')
    local('git merge --no-ff producao')
    roda_teste()
    local('git push -u origin master')
        
def deploy(vNovaVersao=False, vNomeTag=None):
    iDiretorioProducao= '/home/shift/webapps/ged/git/PyProject_GED/'
    iDiretorioApache= '/home/shift/webapps/ged/apache2/bin/'
    iDiretorioApp= '/home/shift/webapps/ged/git/PyProject_GED/src/PyProject_GED/'
    iDiretorioArquivos= '/home/shift/webapps/ged/arquivos/'
    if vNovaVersao:
        print '>>>>>>>>>>>>>>>>>>>> Nova versao'
        checkout('master')
        pull() #master
        roda_teste()
        cria_tag_master(vNomeTag)
        push_tag() #master
        cria_branch()
        push_producao() 
        cria_tag_producao(vNomeTag)
        push_tag() #producao
        clone_producao(iDiretorioProducao)
        checkout_remoto(iDiretorioProducao)
        cria_pastaLog(iDiretorioApp)
        copia_settingsLocal(iDiretorioArquivos, iDiretorioApp)
    else:
        print '>>>>>>>>>>>>>>>>>>>> Versao atual'
        checkout('producao')
        pull() #producao
        roda_teste()
    
    fetch_pull_remoto(iDiretorioProducao)
    #roda_teste_remoto(iDiretorioApp)
    sincronizaBanco_remoto(iDiretorioApp)
    reiniciaApache_remoto(iDiretorioApache)

def scriptInicial(vDiretorio, vIDEmpresa):
    with cd(vDiretorio):
        local('python2.7 manage.py servicos 1 %s' % str(vIDEmpresa)) 
        local('python2.7 manage.py servicos 2 %s' % str(vIDEmpresa)) 
        local('python2.7 manage.py servicos 3 %s' % str(vIDEmpresa)) 
        local('python2.7 manage.py servicos 4 %s' % str(vIDEmpresa)) 
        local('python2.7 manage.py servicos 5 %s' % str(vIDEmpresa)) 

def cria_empresa(vIDEmpresa, vDiretorio, vIDPastaRaiz, vIDPastaModelo):
    iDiretorioDocumentos= '/home/shift/webapps/ged/PyProject_GED/media/documentos/'
    iAliasDataBase= 'empresa_%03d' % int(vIDEmpresa)
    cria_pasta(iDiretorioDocumentos, iAliasDataBase, vIDPastaRaiz, vIDPastaModelo)
    scriptInicial(vDiretorio, vIDEmpresa, iAliasDataBase)


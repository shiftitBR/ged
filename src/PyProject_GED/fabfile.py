from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

import datetime
import xmlrpclib

env.hosts = ['shift@shift.webfactional.com']


def roda_teste():
    with settings(warn_only=True):
        result1 = local('python ./manage.py test autenticacao', capture=True)
    if (result1.failed ) and not confirm("O teste FALHOU! Continuar mesmo assim?"):
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
        local('python2.7 %s%s syncdb --database="%s"' % (vDiretorio, '/manage.py', vDataBase))

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
    
def adiciona_conexao(vIDEmpresa, vDiretorio):
    iArquivo= vDiretorio + '/local_settings.py'
    lines = open(iArquivo).readlines()
    open(iArquivo, 'w').writelines(lines[0:len(lines)-2])
    iAlias= '''    
        },
        'empresa_%02d': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'shift_ged_empresa_%02d',                     
            'USER': 'shift_ged_empresa_%02d',                      
            'PASSWORD': 'ged_db',                  
        }
    }''' 
    open(iArquivo, "a").write(iAlias % (int(vIDEmpresa), int(vIDEmpresa), int(vIDEmpresa)))

def cria_banco(vDataBase):
    iSenha= 'ged_db'
    server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
    session_id, account = server.login('shift', 'shiftit@051011')
    server.create_db(session_id, 'shift_ged_%s' % vDataBase, 'postgresql', iSenha)


def cria_empresa(vIDEmpresa, vDiretorio):
    iDiretorioApache= '/home/shift/webapps/ged/apache2/bin/'
    iAliasDataBase= 'empresa_%02d' % int(vIDEmpresa)
    cria_banco(iAliasDataBase)
    #local('psql -U postgres -c "CREATE DATABASE %s WITH OWNER=%s;"' % (iDataBase, vIDUsuarioBanco))
    adiciona_conexao(vIDEmpresa, vDiretorio)
    reiniciaApache_local(iDiretorioApache)
    sincronizaBanco_local(vDiretorio, iAliasDataBase)
    #migraBanco_local(vDiretorio, iDataBase)


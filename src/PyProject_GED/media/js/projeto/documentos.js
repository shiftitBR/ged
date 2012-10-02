$(document).ready
(
	function()
	{
		//------------------------------OnLoad------------------------------

		if (window.location.pathname == '/documentos/')
		{
			montaArvoreDeDocumentos();
		
			intervaloRefreshDocumentos(300000);
		}
		
		//------------------------------Eventos------------------------------
				
		$('#id_tabelaDocumentos').change(function() {obtemVersoesSelecionadas();});
        
	}
);


//------------------------------Funcoes------------------------------

function refreshDocumentos()
{
	$.post('/tabela_documentos/', { dir: 'teste' }, function(data)
    {
            $("#id_tabelaDocumentos").find("tr:gt(1)").remove();
            $('#id_tabelaDocumentos tr:last').after(data);
    });
}

function montaArvoreDeDocumentos()
{
	$.post('/pasta_raiz/', { dir: 'teste' }, function(data)
    {
		$('#arvore').fileTree({
            root: data,
            script: '/cria_arvore/',
            expandSpeed: 500,
            collapseSpeed: 500,
            multiFolder: false
        });
    });
}

function intervaloRefreshDocumentos(vIntervalo)
{
	setInterval(function(){
        refreshDocumentos()
     }, vIntervalo);
}

function obtemVersoesSelecionadas(vChecks)
{
    var iListaVersoes =  $(':checkbox')
    var iTamanhoLista = iListaVersoes.length;
    var iListaIDVersoes= ''; 
    var iTamanhoListaSelecionadas= 0
    for(i=0;i< iTamanhoLista;i++)
    {
        if (iListaVersoes[i].checked == true)
        { 
            iListaIDVersoes+= iListaVersoes[i].name.substring(7) + '-'; 
            iTamanhoListaSelecionadas ++;
        }
        
    } 
    
    if (iTamanhoListaSelecionadas > 0)
    {
    	$.post('/versoes_selecionadas/'+iListaIDVersoes+'/', { dir: 'teste' }, function(data){});
    }
}
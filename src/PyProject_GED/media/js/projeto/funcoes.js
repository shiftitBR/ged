$(document).ready
(
	function()
	{
	//------------------------------OnLoad------------------------------
		
		placeholder_IE();
		
		intervaloRefreshPendencias(300000);
		
		notificaPendencias();
		
	//------------------------------Eventos------------------------------
		
		if (window.location.pathname == '/importar/')
		{
			$('#id_assunto_importar').keydown(maximoLength('#id_assunto_importar', 100, false));
		}
		
		if (window.location.pathname == '/encaminhar/')
		{
			$('#id_descricao_encaminhar').keypress(maximoLength('#id_descricao_encaminhar', 200, false));
		}
		
		if (window.location.pathname == '/aprovar_documento/')
		{
			$('#aprovar_feedback').keypress(maximoLength('#aprovar_feedback', 200, false));
		}
		
		if (window.location.pathname == '/reprovar_documento/')
		{
			$('#reprovar_feedback').keypress(maximoLength('#reprovar_feedback', 200, false));
		}
		
		if (window.location.pathname == '/checkin/')
		{
			$('#id_descricao_checkin').keypress(maximoLength('#id_descricao_checkin', 200, false));
		}
		
		if (window.location.pathname == '/digitalizar/0/')
		{
			$('#id_assunto_digitalizar').keydown(maximoLength('#id_assunto_digitalizar', 100, false));
		}
		
		if (window.location.pathname == '/importar_lote/')
		{
			$('#id_assunto_lote').keydown(maximoLength('#id_assunto_lote', 100, false));
		}
		
		if ((window.location.pathname).indexOf("visualizar") != -1)
		{
			configuraZoom();
			$('#id_editaimagensinverter').click(function() {inverteImagem();});
			$('#id_editaimagensdireita').click(function() {rotacionaImagem(1);});
			$('#id_editaimagensesquerda').click(function() {rotacionaImagem(2);});
			$('#id_editaimagenszoommais').click(function() {zoomIn();});
			$('#id_editaimagenszoommenos').click(function() {zoomOut();});
		}
	}
);


//------------------------------Funcoes------------------------------


function maximoLength(vCampoID, vTamanho, vStatus)
{
	$(vCampoID).maxlength({   
		events: [], // Array of events to be triggerd    
		maxCharacters: vTamanho, // Characters limit   
		status: vStatus, // True to show status indicator bewlow the element    
		statusClass: "status", // The class on the status div  
		statusText: "caracteres restantes.", // The status text  
		notificationClass: "notificação",	// Will be added when maxlength is reached  
		showAlert: false, // True to show a regular alert message    
		alertText: "Você excedeu o limite de caracteres.", // Text in alert message   
		slider: true // True Use counter slider    
	});
}

function refreshDocumentos(vCampoID)
{
	$.get('/tabela_documentos/', function(data)
    {
            $("#id_tabelaDocumentos").find("tr:gt(1)").remove();
            $('#id_tabelaDocumentos tr:last').after(data);
    });
}

function placeholder_IE()
{ 
	jQuery(function(){
		jQuery.support.placeholder = false;
		test = document.createElement('input');
		if('placeholder' in test) jQuery.support.placeholder = true;
	});
	$(function() {
		if(!$.support.placeholder) { 
			$(':input').focus(function () {
				if ($(this).attr('placeholder') != '' && $(this).val() == $(this).attr('placeholder')) {
					$(this).val('').removeClass('hasPlaceholder');
				}
			}).blur(function () {
				if ($(this).attr('placeholder') != '' && ($(this).val() == '' || $(this).val() == $(this).attr('placeholder'))) {
					$(this).val($(this).attr('placeholder'));
					$(this).addClass('hasPlaceholder');
				}
			});
			$(':input').blur();
			$('form').submit(function () {
				$(this).find('.hasPlaceholder').each(function() { $(this).val(''); });
			});
		}
	});
}

function notificaPendencias()
{
	$.get('/quantidade_pendencias/', function(data)
    {
		if(data != '0')
		{
			$('#id_notificapendencia').text(data);
		}
		else
		{
			$('#id_notificapendencia').remove();
		}
		
    });
}

function intervaloRefreshPendencias(vIntervalo)
{
	setInterval(function(){
		notificaPendencias()
     }, vIntervalo);
}

function inverteImagem()
{
	$.post('/negativar_imagem/', function(data){
		d = new Date();
		$("#id_img-polaroid").attr("src", data+'?'+d.getTime());
		
	});
	
}

function rotacionaImagem(vLado)
{
	$.post('/rotacionar_imagem/'+vLado+'/', function(data){
		d = new Date();
		$("#id_img-polaroid").attr("src", data+'?'+d.getTime());
		
	});
}

function configuraZoom()
{
	$('#id_img-polaroid').smoothZoom({
        width: '100%',
        height: '100%',
        zoom_BUTTONS_SHOW : 'NO',
        pan_BUTTONS_SHOW : 'NO',
        pan_LIMIT_BOUNDARY : 'YES',
        background_COLOR: 'transparent',
        border_TRANSPARENCY: 0
    });
}


function zoomIn()
{
	$('#id_img-polaroid').smoothZoom('zoomIn');
}

function zoomOut()
{
	$('#id_img-polaroid').smoothZoom('zoomOut');
}
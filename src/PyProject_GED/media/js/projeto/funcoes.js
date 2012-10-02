$(document).ready
(
	function()
	{
	//------------------------------OnLoad------------------------------
		
		placeholder_IE();
		
	//------------------------------Eventos------------------------------
		
		if (window.location.pathname == '/importar/')
		{
			$('#id_assunto_importar').keydown(maximoLength('#id_assunto_importar', 100, true));
		}
		
		if (window.location.pathname == '/encaminhar/')
		{
			$('#id_descricao_encaminhar').keypress(maximoLength('#id_descricao_encaminhar', 200, true));
		}
		
		if (window.location.pathname == '/aprovar_documento/')
		{
			$('#aprovar_feedback').keypress(maximoLength('#aprovar_feedback', 200, true));
		}
		
		if (window.location.pathname == '/reprovar_documento/')
		{
			$('#reprovar_feedback').keypress(maximoLength('#reprovar_feedback', 200, true));
		}
		
		if (window.location.pathname == '/checkin/')
		{
			$('#id_descricao_checkin').keypress(maximoLength('#id_descricao_checkin', 200, true));
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
	$.post('/tabela_documentos/', { dir: 'teste' }, function(data)
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
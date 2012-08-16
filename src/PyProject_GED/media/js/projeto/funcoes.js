$(document).ready
(
	function()
	{
	//------------------------------Eventos------------------------------
		
		$('#id_descricao_encaminhar').keypress(maximoLength('#id_descricao_encaminhar', 200, true));
		
		$('#aprovar_feedback').keypress(maximoLength('#aprovar_feedback', 200, true));
		
		$('#reprovar_feedback').keypress(maximoLength('#reprovar_feedback', 200, true));
		
		$('#id_assunto_importar').keypress(maximoLength('#id_assunto_importar', 100, true));
		
		$('#id_descricao_checkin').keypress(maximoLength('#id_descricao_checkin', 200, true));
		
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
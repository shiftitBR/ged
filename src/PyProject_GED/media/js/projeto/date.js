
$('#datavalidade').DatePicker({
	format:'m/d/Y',
	date: $('#datavalidade').val(),
	current: $('#datavalidade').val(),
	starts: 1,
	position: 'r',
	onBeforeShow: function(){
		$('#datavalidade').DatePickerSetDate($('#datavalidade').val(), true);
	},
	onChange: function(formated, dates){
		$('#datavalidade').val(formated);
		if ($('#closeOnSelect input').attr('checked')) {
			$('#datavalidade').DatePickerHide();
		}
	}
});




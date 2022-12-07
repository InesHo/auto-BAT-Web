$(document).ready(function(){
	var ShowFiles = function(){
		var btn = $(this);

		$.ajax({
			url: btn.attr("data-url"),
			beforeSend: function(){
				$('#modal-analysis').modal('show');
			},
			success: function(data){
				$('#modal-analysis .modal-content').html(data.html_form);
			}
		});
	};

//Show Files
$(".show-files").click(ShowFiles);

});
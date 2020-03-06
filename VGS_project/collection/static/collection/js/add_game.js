$("div#answer").hide();
$("button#restart").hide();
$("p#middlebar").hide();
$("input#adress").focus();

$("button#send").on("click", function(event) {

	$.ajax({
		data : {
			question : $("#question").val()
		},
		type : "POST",
		url : "/process"
	});

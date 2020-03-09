$("div#ga").hide();
$("div#comp").hide();

$("button#game").on("click", function(event) {
    $("div#ga").show();
    $("div#comp").hide();
});
$("button#compilation").on("click", function(event) {
    $("div#comp").show();
    $("div#ga").hide();
});

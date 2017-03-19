var time = 0;
setInterval(function(){
  var now = (30 - ++time);
  document.getElementById("timer").textContent = (now>=0 ? now : 0) ;
},1000);

$(function(){
    $("#accordion >li").accordion({
      active: false,
      collapsible: true
    });

});

$(document).ready(function(){

	$("#accordion >li").accordion("option", "active", 0 );

	$("#collapse").click(function(){
		$("#accordion >li").accordion("option", "active", false );
	});

	$("#expand").click(function(){
		$("#accordion >li").accordion("option", "active", 0 );
	});


	$(".progress-bar").each(function(){

		var progress = $(this).attr('progress');
		$(this).css('width',progress);

		var prog_val = parseInt(progress.substring(0, progress.length-1));

		if(prog_val > 75){
			console.log("hello");
			$(this).css('background-color', '#49ff28');
		}
		else if(prog_val > 40){
			$(this).css('background-color', 'yellow');
		}
		else{
			$(this).css('background-color', 'red');
		}

	});

});

$(function(){

    $("#accordion >li").accordion({
	  beforeActivate: function( event, ui ) {
	  		$(this).toggleClass("selected");	
	  }
	});

});


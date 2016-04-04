$('.c .right .buttons .bike').click(function(){

	$('.c .right .buttons .select').removeClass('active');
	$('.c .right .buttons .bike').addClass('active');
	$('.c .left').removeClass('bike car show');
	$('.c .left').addClass('bike show');
	$('.c .right .info .content').removeClass('active');
	$('.c .right .info .bike').addClass('active');
});

$('.c .right .buttons .car').click(function(){
	$('.c .right .buttons .select').removeClass('active');
	$('.c .right .buttons .car').addClass('active');
	$('.c .left').removeClass('bike car show');
	$('.c .left').addClass('car show');
	$('.c .right .info .content').removeClass('active');
	$('.c .right .info .car').addClass('active');
});
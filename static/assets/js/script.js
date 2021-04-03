(function($) {
    "use strict";
	
 	/*  Navbar */
    $(window).on('scroll load', function() {
		if ($(".navbar").offset().top > 100) {
			$(".fixed-top").addClass("top-nav-collapse");
		} else {
			$(".fixed-top").removeClass("top-nav-collapse");
		}
    });
	
	// jQuery for page scrolling feature - requires jQuery Easing plugin
	$(function() {
		$(document).on('click', 'a.page-scroll', function(event) {
		var $anchor = $(this);
		$('html, body').stop().animate({
			scrollTop: $($anchor.attr('href')).offset().top
			}, 3000, 'easeInOutExpo');
			event.preventDefault();
		});
	});
	
	// Back Top Link acive   
      var amountScrolled = 200;
    $(window).scroll(function() {
        if ($(window).scrollTop() > amountScrolled) {
            $('a.back-to-top').fadeIn('500');
        } else {
            $('a.back-to-top').fadeOut('500');
        }
    });
     

})(jQuery);



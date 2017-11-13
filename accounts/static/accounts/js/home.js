jQuery( document ).ready(function() {
jQuery('.client-list').slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        arrows: false,
        dots: false,
          pauseOnHover: true,
          responsive: [{
          breakpoint: 768,
          settings: {
            slidesToShow: 3
          }
        }, {
          breakpoint: 520,
          settings: {
            slidesToShow: 2
          }
        },]
      });
  jQuery(document).scroll(function(){
    jQuery(this).scrollTop() > 150 ? jQuery('header').addClass('header-sticky') : jQuery('header').removeClass('header-sticky');
      if(happenOnce1 && jQuery(this).scrollTop() > talentHeight){swingNumbers(1); happenOnce1 = false;};
      if(happenOnce2 && jQuery(this).scrollTop() > domainHeight){swingNumbers(2); happenOnce2 = false;};
  });
  if (jQuery(".counter-block-1")[0]){
  var talentHeight = jQuery('.counter-block-1').offset().top - 240,
      domainHeight = jQuery('.counter-block-2').offset().top - 240,
      happenOnce1 = true,
      happenOnce2 = true;
  }

  function swingNumbers(counterId){
    jQuery('.counter' + counterId).each(function () {
      asd=jQuery(this).attr('val');
      jQuery(this).prop('Counter',0).animate({
          Counter: asd
      }, {
          duration: 2000,
          easing: 'swing',
          step: function (now) {
              jQuery(this).text(Math.ceil(now)+" +");
          }
      });
    });
  }



/* About page */

jQuery(".team .read-more").click(function() {
  var prev = jQuery(this).prev(".description");
  prev.toggleClass('show');
  prev.hasClass('show')? jQuery(this).text("Show Less"):jQuery(this).text("Show More"); 
});   
function bannerFunction() {
  var xyz = setInterval(function() {
  var currentPulse = jQuery('.circle.pulse');
  var nextElem = currentPulse.next();
  if(nextElem.length === 0) {
  nextElem = jQuery('.circ-1');
  }
  currentPulse.removeClass('pulse');
  nextElem.addClass('pulse');
  if(nextElem.hasClass('circ-hold')) {
  clearTimeout(xyz);
  setTimeout(function() {
  nextElem.removeClass('pulse');
  nextElem = nextElem.next();
  nextElem.addClass('pulse');
  bannerFunction();
  },2000);
  return;
  }
  },1000);
  };
  jQuery(document).ready(function() {
  jQuery('.circ-1').addClass('pulse');
  bannerFunction();
  });

/* Case study */
jQuery("showcase-slider:first-child").addClass('active');
});
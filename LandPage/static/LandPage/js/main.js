/*
    Project Name : Proff
    Author Company : SpecThemes
    Project Date: 25 July, 2017
    Template Developer: vsafaryan50yan@gmail.com
*/


/*
==============================================
TABLE OF CONTENT
==============================================

1. Owl Carousels
2. CountUp
3. Hover Drop Down
4. Tabs
5. Video Modal
6. Preloader
7. Smooth Scroll (Landing)
8. Isotop
9. WOW


==============================================
[END] TABLE OF CONTENT
==============================================
*/


$(document).ready(function() {

/*------------------------------------
    1. Owl Carousel
--------------------------------------*/  


/*---------------------
Top Articles carousel
-----------------------*/

  $('#articles-services').owlCarousel({
    loop: false,
    nav: false,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
        margin: 30,
      },
      600: {
        items: 2,
        margin: 30,
      },
      1000: {
        items: 3,
        margin: 30,
      }
    }
  })


/*---------------------
Testmonials carousel
-----------------------*/

  $('#testmonials').owlCarousel({
    loop: false,
    nav: false,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
        margin: 30,
      },
      600: {
        items: 1,
        margin: 30,
      },
      1000: {
        items: 2,
        margin: 60,
      }
    }
  })


/*---------------------
Partners carousel
-----------------------*/

  $('#our-partners').owlCarousel({
    loop: true,
    nav: false,   
    dots: false,
    responsiveClass: true,
    // margin: 100,
    responsive: {
      0: {
        items: 2,
        margin: 15,
      },
      600: {
        items: 3,
        margin: 15,
      },
      1000: {
        items: 5,
        margin: 15,
      }
    }
  })


/*------------------------------------
    2. CountUp
--------------------------------------*/  

    $('.countup').counterUp({
        delay: 5,
        time: 2000
    });


/*------------------------------------
    3. Hover Drop Down
--------------------------------------*/    

if ($(window).width() > 992) {
  $('ul.nav li.dropdown').hover(function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(300);
  }, function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(300);
  });
}


/*------------------------------------
    4. Tabs
--------------------------------------*/    

  $('.tabs_animate').tabslet({
    mouseevent: 'click',
    attribute: 'href',
    animation: true
  });


/*------------------------------------
    5. Video Modal
--------------------------------------*/ 

  $('#videomodal').on('hidden.bs.modal', function() {
    var $this = $(this).find('iframe'),
      tempSrc = $this.attr('src');
    $this.attr('src', "");
    $this.attr('src', tempSrc);
  });

  $('#videomodal').on('hidden.bs.modal', function() {
    var html5Video = document.getElementById("htmlVideo");
    if (html5Video != null) {
      html5Video.pause();
      html5Video.currentTime = 0;
    }
  });


/*------------------------------------
    6. Preloader
--------------------------------------*/ 

  $('#preloader').fadeOut('normall', function() {
      $(this).remove();
  });


/*------------------------------------
    7. Smooth Scroll
--------------------------------------*/ 
    $(document).on("scroll", onScroll);
    "use strict";
    //smoothscroll
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        $(document).off("scroll");
        
        $('a').each(function () {
            $(this).removeClass('active-nav');
        })
        $(this).addClass('active-nav');
      
        var target = this.hash,
            menu = target;
        $target = $(target);
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top-20
        }, 800, 'swing', function () {
            window.location.hash = target;
            $(document).on("scroll", onScroll);
        });
    });


    function onScroll(event){
        var scrollPos = $(document).scrollTop();
        $('#bs-example-navbar-collapse-1 ul li a').each(function () {
            var currLink = $(this);
            var refElement = $(currLink.attr("href"));
            if (refElement.position().top-89.5 <= scrollPos && refElement.position().top+89.5 + refElement.height() > scrollPos) {
                $('#bs-example-navbar-collapse-1 ul li a').removeClass("active-nav");
                currLink.addClass("active-nav");
            }
            else{
                currLink.removeClass("active-nav");
            }
        });
    }



/*------------------------------------
    8. Isotop
--------------------------------------*/  

// external js: isotope.pkgd.js
// init Isotope
var $grid = $('.isotope-grid').isotope({
  itemSelector: '.isotope-item',
  layoutMode: 'fitRows',
  getSortData: {
    name: '.name',
    symbol: '.symbol',
    number: '.number parseInt',
    category: '[data-category]',
    weight: function( itemElem ) {
      var weight = $( itemElem ).find('.weight').text();
      return parseFloat( weight.replace( /[\(\)]/g, '') );
    }
  }
});

// filter functions
var filterFns = {
  // show if name ends with -ium
  ium: function() {
    var name = $(this).find('.name').text();
    return name.match( /ium$/ );
  }
};

// bind filter button click
$('#filters').on( 'click', 'button', function() {
  var filterValue = $( this ).attr('data-filter');
  // use filterFn if matches value
  filterValue = filterFns[ filterValue ] || filterValue;
  $grid.isotope({ filter: filterValue });
});


// change is-checked class on buttons
$('.latest-projects').each( function( i, buttonGroup ) {
  var $buttonGroup = $( buttonGroup );
  $buttonGroup.on( 'click', 'button', function() {
    $buttonGroup.find('.is-checked').removeClass('is-checked');
    $( this ).addClass('is-checked');
  });
});



/*------------------------------------
    10. WOW
--------------------------------------*/ 
new WOW().init();


});
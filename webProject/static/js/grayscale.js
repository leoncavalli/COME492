(function ($) {
  "use strict";

  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 70)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function () {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 100
  });

  // Collapse Navbar
  var navbarCollapse = function () {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

})(jQuery); // End of use strict


//Responsive navbar js ops


function openNav() {
  $('.sidenav').addClass('nav-width75');
  $('.sidenav').removeClass('nav-width');

}

function closeNav() {
  $('.sidenav').removeClass('nav-width75');
  $('.sidenav').addClass('nav-width');
}

var dropdown = document.getElementsByClassName('respDrpdwn');
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function (e) {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;

    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
      e.preventDefault();

    }
  });
}

//Choose Model Page js ops

var introCard = $('#cardIntro .card');

introCard.hover(
  function () {

    $(this).addClass("introActive");

  },
  function () {

    $(this).removeClass("introActive");


  });


//Range slider 

$(function () {
  var $document = $(document),
    $inputRange = $('input[type="range"]');

  // Example functionality to demonstrate a value feedback
  function valueOutput(element) {
    var value = element.value,
      output = element.parentNode.getElementsByTagName('output')[0];
    output.innerHTML = value + "$";
  }
  for (var i = $inputRange.length - 1; i >= 0; i--) {
    valueOutput($inputRange[i]);
  };
  $document.on('input', 'input[type="range"]', function (e) {
    valueOutput(e.target);
  });
  // end

  $inputRange.rangeslider({
    polyfill: false,
  });
});

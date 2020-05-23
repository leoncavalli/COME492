$(document).ready(function () {

  $("#signup").on("keyup", "form", function (e) {
    if (e.which == 13) {
      if ($("#next").is(":visible") && $("fieldset.current").find("input, textarea").valid()) {
        e.preventDefault();
        nextSection();
        return false;
      }
    } 
  });

  $("#next").on("click", function (e) {
    console.log(e.target);
    nextSection();
  });

  $("#stepForm").on("submit", function (e) {
    if ($("#next").is(":visible") || $("fieldset.current").index() < 3) {
      e.preventDefault();
    }
  });

  function goToSection(i) {
    $("fieldset:gt(" + i + ")").removeClass("current").addClass("next");
    $("fieldset:lt(" + i + ")").removeClass("current");
    $("#section-tabs li").eq(i).addClass("current").siblings().removeClass("current");
    setTimeout(function () {
      $("fieldset").eq(i).removeClass("next").addClass("current active");
      if ($("fieldset.current").index() == 3) {
        $("#next").hide();
        $("input[type=submit]").show();
      } else {
        $("#next").show();
        $("input[type=submit]").hide();
      }
    }, 80);

  }

  function nextSection() {
    var i = $("fieldset.current").index();
    if (i < 3) {
      $("#section-tabs li").eq(i + 1).addClass("active");
      goToSection(i + 1);
    }
  }

  $("#section-tabs li").on("click", function (e) {
    var i = $(this).index();
    if ($(this).hasClass("active")) {
      goToSection(i);
    } else {
      alert("Please complete sections first.");
    }
  });

})
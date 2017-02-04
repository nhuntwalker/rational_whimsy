$(document).ready(function(){
   var menu_btn = $("#menu-btn");
   menu_btn.on("click", function(){
        var mobile_menu = $("#mobile-menu");
        if (mobile_menu.hasClass("dropped")) {
            $("#mobile-menu").animate({
                "margin-top": "-100%"
            }, 500).removeClass("dropped");
        } else {
            $("#mobile-menu").animate({
                "margin-top": "-1.5%",
            }, 500).addClass("dropped");
        }
   }); 
});
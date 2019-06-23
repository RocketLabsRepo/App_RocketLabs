// Modal Image Gallery
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}


// Toggle between showing and hiding the sidebar when clicking the menu icon
var mySidebar = document.getElementById("mySidebar");

function w3_open() {
    if (mySidebar.style.display === 'block') {
        mySidebar.style.display = 'none';
    } else {
        mySidebar.style.display = 'block';
    }
}

// Close the sidebar with the close button
function w3_close() {
    mySidebar.style.display = "none";
}


$(document).ready(function(){

  // Script para añadir un efecto de fadeIn al texto de 'about'
  $(window).scroll(function () {
    /* Check the location of each desired element to fade in */
    $('.fadeInOnScroll').each( function(i){
      var bottom_of_object = $(this).offset().top + $(this).outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      /* If the object is completely visible in the window, fade it it */
      if( bottom_of_window > bottom_of_object ){

          $(this).animate({'opacity':'1'},600);
      }
    });


  });

  //Script para efecto de hover de los paquetes.
  $("div.bundle").hover(function(){
    //$(this).removeClass(" w3-section ");
    $(this).animate({top:'-=30'}, 200);
    }, function(){
    //$(this).addClass(" w3-section ");
    $(this).animate({top:'+=30'}, 200);
});


  //Script para desplegar los detalles de un proyecto en el panel de control.
  $('button.toggle-project-details').on( "click", function(){
    var $target_icon = $( this ).find('i');
    var $target_details = $( this ).closest('div').find('div.project-details');

    // If it's closed and the chevron is pointing right, remove that class, add
    // fa-chevron-down and slide down the sibling div.project-details
    // If it's open and the chevron is pointing down, remove that class and add
    // fa-chevron-right.
    $target_icon.toggleClass('fa-chevron-down fa-chevron-right');
    $target_details.slideToggle();
  });

});
/* Project specific Javascript goes here. */
$(".close").on("click", function(){
  $(".alert").remove();
});

$('.sidenav-trigger').on("click", function(){
    $('.sidenav').css('transform', 'translateX(0%)');
})

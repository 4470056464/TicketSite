$('.message a').click(function(){
    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
 });
 
setTimeout(function(){
    $('#message').fadeOut('slow');
  },3000);
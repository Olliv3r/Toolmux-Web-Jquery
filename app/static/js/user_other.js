$(document).ready(function() {
  load_user_other();
  load_image();

  // Carrega informaçôes do usuário  
  function load_user_other() {
    $.ajax({
      url: '/get-user-other',
      type: 'GET',
      data: {'username': $("#username").val()},
      success: function(response) {
        $("#user-other").html(response.user_other);
      }
    });
  }

  // Carrega imagem no perfil
  function load_image() {
    let user_id = $(".user #user_id").val();
    let default_image = "https://bootdey.com/img/Content/avatar/avatar7.png";
	  
    $.ajax({
      url: "/get-image",
      data: {"user_id": user_id},
      type: "GET",
      success: function(response) {
        if (response.process === false) {
          $(".personal-figure img").attr("src", default_image);
        }
	  }
	});
  }
  
  
});

$(document).ready(function() {
  load_profile();
  load_image();
  
  var cropData;

  // Carrega informaçôes no perfil
  function load_profile() {
    $.ajax({
      url: '/get-profile',
      type: 'GET',
      success: function(response) {
	    $("#profile").html(response.profile);
	  }
	});
  }
  
  // Carrega imagem no perfil
  function load_image() {
    let user_id = $(".profile #user_id").val();
  	let default_image = "https://bootdey.com/img/Content/avatar/avatar7.png";
	  
    $.ajax({
      url: "/get-image",
      data: {"user_id": user_id},
      type: "GET",
      success: function(response) {
        if (response.process === false) {
          $("#previewImage").attr("src", default_image);
        }
	  }
	});
  }

  // Evento de envio do formulário dos campos
  $("#profile").on("submit", "#profileEditForm", function(event) {
    event.preventDefault();
    $button = $(this);
    $button.attr("disabled", true);
    
    $.ajax({
  	  url: "/edit-profile-user",
  	  type: "POST",
  	  data: {
  	    "username": $("#profileEditForm #profile_username").val(),
  	    "name": $("#profileEditForm #name").val(),
        "email": $("#profileEditForm #email").val(),
        "website": $("#profileEditForm #website").val(),
        "profission": $("#profileEditForm #profission").val(),
        "address": $("#profileEditForm #address").val(),
        "github": $("#profileEditForm #github").val()
  	  },
  	  success: function(response) {
  	  	$("#message").addClass("alert alert-warning");
  	    $("#message").html(response.msg);
  	    $button.attr("disabled", false);
  	    load_profile();
  	    load_image();
  	  }
  	});
    
  	setTimeout(function() {
      $("#message").removeClass("alert alert-warning");
      $("#message").html("");
    }, 5000);
  });

  // Carrega uma visualização prévia do avatar
  $("#profile").on("change", "#profileForm #fileInput", function(event) {
    event.preventDefault();
    var input = this;
  
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      
      reader.onload = function(e) {
        $("#previewImage").attr("src", e.target.result);

      };
      reader.readAsDataURL(input.files[0]);
    }
  });
  
  // Evento de envio da foto do perfil
  $("#profile").on('submit', "#profileForm", function(event) {
    event.preventDefault();
    $button = $(this);
    $button.attr("disabled", true);

    var fileInput = $("#fileInput")[0];

    if (fileInput.files.length > 0) {
    
      let formData = new FormData($(this)[0]);
      formData.append('user_id', $("#profileForm #user_id").val());
    
      $.ajax({
        url: "/upload",
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
          if (response.status == "404") {
          	return;
          } else if (response.status == "400") {
          	$("#message").addClass("alert alert-danger");
  	        $("#message").html(response.msg);
  	        load_image();
          } else {
            load_image();
          }
          $button.attr("disabled", false);
          $("#message").addClass("alert alert-success");
  	      $("#message").html(response.msg);
        }
      });
      
    } else {
      $("#message").addClass("alert alert-danger");
      $("#message").html("Selecione uma nova imagem");
      $button.attr("disabled", false);
    }

    setTimeout(function() {
      $("#message").removeClass("alert alert-primary");
      $("#message").removeClass("alert alert-danger");
      $("#message").html("");
    }, 5000);
  });

  
});

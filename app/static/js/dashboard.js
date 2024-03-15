$(document).ready(function() {
  var $dashboardContent = $("#dashboard-content");
  
  // Modais de usuário
  var $modalAddUser = $("#modalAddUser");
  var $modalEditUser = $("#modalEditUser");
  var $modalViewUser = $("#modalViewUser");
  var $modalDeleteUser = $("#modalDeleteUser");
  
  // Modais de ferramenta
  var $modalAddTool = $("#modalAddTool");
  var $modalEditTool = $("#modalEditTool");
  var $modalViewTool = $("#modalViewTool");
  var $modalDeleteTool = $("#modalDeleteTool");
  
  // Formulários de ferramenta
  var $formAddTool = $("#add-tool-form");
  var $formEditTool = $("#edit-tool-form");
  
  // Formulários de usuário
  var $formAddUser = $("#add-user-form");
  var $formEditUser = $("#edit-user-form");
  
  // Carrega por padrão o conteúdo do painel 
  load_dashboad_home();
  
  // Função para carregar conteúdo padrão do dashboard
  function load_dashboad_home() {
    $.ajax({
      url: '/get-dashboard-home',
      type: 'GET',
      success: function(response) {
        $("[data-action-button]").hide();
        $(".content .title").html(response.title);
        $("#dashboard-content").html(response.dashboard_home);
      }
    });
  }
  
  // Função para carregar usuários no painel
  function load_dashboad_user() {
    var $button = $(".content [data-action-button]");
    
    $.ajax({
      url: '/get-dashboard-user',
      type: 'GET',
      success: function(response) {
        $button.show();
        $button.attr("data-target", "#modalAddUser");
        $(".content .title").html(response.title);
        $dashboardContent.html(response.dashboard_user);
      }
    });
  }
  
  // Função para carregar ferramentas no painel
  function load_dashboad_tool() {
    var $button = $(".content [data-action-button]");
    
    $.ajax({
      url: '/get-dashboard-tool',
      type: 'GET',
      success: function(response) {
        $button.show();
        $button.attr("data-target", "#modalAddTool");
        $(".content .title").html(response.title);
        $dashboardContent.html(response.dashboard_tool);
      }
    });
  }

  // Evento de tecla ao digitar na pesquisa
  /*
  $("#search_text").on("keyup", function() {
    var keyword = $(this).val();
    
    if (keyword !== "") {
      load_search_users();
    } else {
      load_users();
    }
  });
  */
  
  // Função para carregar usuários pesquisados
  /*
  function load_search_users() {
    $.ajax({
      url: "/search-users",
      type: "GET",
      data: {'search_text': $("#search_text").val()},
      success: function(response) {
        $("#tableUsers").html(response.search_users);
      }
    });
  }
  */

  // Eventos de clique para paginar usuários e ferramentas
  
  $dashboardContent.on("click", "[data-page-prev-user], [data-page-next-user], [data-page-prev-tool], [data-page-next-tool]", function() {
    var page_url = $(this).data("page-prev-user") || $(this).data("page-next-user") || $(this).data("page-next-tool") || $(this).data("page-prev-tool");
    paginate(page_url);
  });
  
  // Função para paginar usuários e ferramentas
  
  function paginate(page_url) {
    $.ajax({
      url: page_url,
      type: "GET",
      success: function(response) {
        $dashboardContent.html(response.dashboard_user || response.dashboard_tool);
      }
    });
  }

  // Evento de clique que abre e fecha o menu
  $(".sidebar-toggle").on("click", function() {
    $(".sidebar").toggleClass("toggled");
  });
  
  /*
  // Define cor de fundo do item ativo
  var active = $(".sidebar .active");
  if (active.length && active.parent('.collapse').length) {
    var parent = active.parent('.collapse');
    
    parent.prev('a').attr("aria-expanded", true);
    parent.addClass("show");
  }
  */
  
  // Carrega conteúdo padrão no painel
  $("[data-dashboard]").on("click", function() {
    load_dashboad_home();
  });
  
  // Carrega usuários no painel
  $("[data-user]").on("click", function() {
    load_dashboad_user();
  });
  
  // Carrega ferramentas no painel
  $("[data-tool]").on("click", function() {
    load_dashboad_tool();
  });
  
  // Evento de shown.bs.modal que preenche os campos de ferramenta com valores padrão quando a modal #modalAddUser é exibida
  $modalAddUser.on("shown.bs.modal", function(e)  {
    $(".situationsusers").html("");
    $(".roles").html("");
    
    $.ajax({
      url: "/get-data-sr",
      type: "GET",
      success: function(response) {
        response.situationsusers.forEach(situationuser => {
          $(".situationsusers").append('<option value="'+situationuser.id+'">'+situationuser.name+'</option>');
        });
        $(".situations #situationuser").val("1");
        response.roles.forEach(role => {
          $(".roles").append('<option value="'+role.id+'">'+role.name+'</option>');
        });
        $(".roles #role").val("1");
      }
    });
    
    $formAddUser.find("#email").on("change", function() {
      var $message = $formAddUser.find("#message_email");
      var email = $(this).val();
      
      $.ajax({
        url: '/validate-email',
        type: 'POST',
        data: {'email': email},
        success: function(response) {
          if (response.exists === true) {
            $message.text("E-mail inválido!");
          } else {
            $message.text("E-mail válido!");
          }
        }
      });
    });
    $formAddUser.find("#username").on("change", function() {
      var $message = $formAddUser.find("#message_username");
      var username = $(this).val();
      
      $.ajax({
        url: '/validate-username',
        type: 'POST',
        data: {'username': username},
        success: function(response) {
          if (response.exists === true) {
            $message.text("Usuário inválido!");
          } else {
            $message.text("Usuário válido!");
          }
        }
      });
    });
    $formAddUser.find("#password2").on("change", function() {
      var $message = $formAddUser.find("#message_password");
      var $password = $formAddUser.find("#password");
      var password2 = $(this).val();
      
      if ($password.val() !== password2) {
        $message.text("As senhas não são iguais!");
      } else {
        $message.text("As senhas são iguais!");
      }
    });
  });
  
  function validate_email(email) {
    $.ajax({
      url: '/validate-email',
      type: 'POST',
      data: {'email': email},
      success: function(response) {
        return response.exists;
      }
    });
  }
  function validate_username(username) {
    $.ajax({
      url: '/validate-username',
      type: 'POST',
      data: {'username': username},
      success: function(response) {
        return response.exists;
      }
    });
  }
  
  // Evento de submit que adiciona um usuário
  $modalAddUser.on("submit", function(event) {
    event.preventDefault();
    var $message = $("#message");
    var $button = $modalAddUser.find("[data-btn-add]");
    var confirmed = $formAddUser.find("#confirmed").is(":checked") ? true : false;

    $button.attr("disabled", true);
    $button.text("Aguarde...");
    
    if ($formAddUser.find("#password").val() === $formAddUser.find("#password2").val()) {
      
      var formData = new FormData($formAddUser[0]);
      formData.append('confirmed', confirmed);

      $.ajax({
    	  url: "/add-user",
    	  type: "POST",
    	  data: formData,
    	  processData: false,
    	  contentType: false,
    	  success: function(response) {
    	    $formAddUser[0].reset();
    	    $button.attr("disabled", false);
    	    $button.text("Adicionar");
    	  	$modalAddUser.modal("hide");
    	  	$message.addClass(response.alert);
    	    $message.html(response.msg);
    	  	load_dashboad_user();
    	  }
    	});
    }
    else {
      $("#message_password").text("As senhas não correspondem!");
      $button.attr("disabled", false);
      $button.text("Adicionar");
    }
    
  	setTimeout(function() {
      $message.removeClass("alert alert-primary");
      $message.html("");
    }, 5000);
  });
 
  // Evento de clique que visualiza um usuário
  $dashboardContent.on("click", "[data-view-user-id]", function() {
    var id = $(this).data("view-user-id");
  
    $.ajax({
      url: "/view-user",
      data: {"user_id": id},
      type: "GET",
      success: function(response) {
        $modalViewUser.find(".modal-body").html(response.view_user_response);
        $modalViewUser.find("#created").html(moment.utc($modalViewUser.find("#created").html()).fromNow());
        $modalViewUser.find("#modified").html(moment.utc($modalViewUser.find("#modified").html()).fromNow());
      }
    });
  });
  
  // Evento de clique que seleciona um usuário para ser editado
  $dashboardContent.on("click", "[data-edit-user-id]", function() {
    var user_id = $(this).data("edit-user-id");
    
    $formEditUser.find(".situationsusers").html("");
    $formEditUser.find(".roles").html("");
    
    $.ajax({
      url: "/get-data-user",
      type: "GET",
      data: {"user_id": user_id},
      success: function(response) {
        $formEditUser.find("#username").val(response.username);
        $formEditUser.find("#email").val(response.email);
        response.situationsusers.forEach(situationuser => {
          $formEditUser.find(".situationsusers").append('<option value="'+situationuser.id+'">'+situationuser.name+'</option>');
        });
        $formEditUser.find("#situationuser").val(response.situation_user_id);
        
        response.roles.forEach(role => {
          $formEditUser.find(".roles").append('<option value="'+role.id+'">'+role.name+'</option>');
        });
        $formEditUser.find("#role").val(response.role_id);
        $formEditUser.find("#confirmed").prop("checked", response.confirmed);
      }
    });
    $modalEditUser.find("[data-btn-edit]").val(user_id);
  });

	// Evento de submit que edita um usuário
  $formEditUser.on("submit", function(event) {
    event.preventDefault();
    var $message = $("#message");
    
    var $button = $modalEditUser.find("[data-btn-edit]");
    var confirmed = $formEditUser.find("#confirmed").is(":checked") ? true : false;
    var user_id = $button.val();
    
    $button.attr("disabled", true);
    $button.text("Aguarde...");
    
    if ($formEditUser.find("#password").val() === $formEditUser.find("#password2").val()) {
      var formData = new FormData($formEditUser[0]);
      formData.append('confirmed', confirmed);
      formData.append('user_id', user_id);
    
      $.ajax({
    	  url: "/edit-user",
    	  type: "POST",
    	  data: formData,
    	  processData: false,
    	  contentType: false,
    	  success: function(response) {
    	  	$modalEditUser.modal("hide");
    	  	$message.addClass("alert alert-warning");
    	    $message.html(response.msg);
    	    $button.attr("disabled", false);
    	    $button.text("Editar");
    	  	load_dashboad_user();
    	  }
    	});
    } else {
      alert("Senha não corresponde!");
      $button.attr("disabled", false);
      $button.text("Editar");
    }
  
    setTimeout(function() {
      $message.removeClass("alert alert-warning");
      $message.html("");
    }, 5000);
  });

  // Evento de clique que seleciona um usuário para ser deletado
  $dashboardContent.on("click", "[data-delete-user-id]", function() {
    var id = $(this).data("delete-user-id");
    $("[data-btn-delete]").val($(this).data("delete-user-id"));
  });
  
  // Evento de clique que deleta um usuário
  $modalDeleteUser.on("click", "[data-btn-delete]", function() {
    var $message = $("#message");
    var $button = $modalDeleteUser.find("[data-btn-delete]");
    
    $button.attr("disabled", true);
    $button.text("Aguarde...");
    
    $.ajax({
      url: "/delete-user",
      type: "POST",
      data: {"user_id": $button.val()},
      success: function(response) {
        $modalDeleteUser.modal("hide");
        $button.attr("disabled", false);
        $button.text("Confirmar");
        $message.addClass("alert alert-success");
  	    $message.html(response.msg);
  	  	load_dashboad_user();
      }
    });
    
    setTimeout(function() {
      $message.removeClass("alert alert-success");
      $message.html("");
    }, 5000);
  });
  
  // Evento de shown.bs.modal que preenche campos de ferramenta com valores padrão quando a modal #modalAddTool é exibida
  $modalAddTool.on("shown.bs.modal", function() {
    $modalAddTool.find("#link").on("keyup", function() {
      $modalAddTool.find("#author").val($modalAddTool.find("#link").val().split("/").slice(3,4));
      $modalAddTool.find("#alias").val($modalAddTool.find("#link").val().split("/").slice(4,));
      $modalAddTool.find("#name_repo").val($modalAddTool.find("#link").val().split("/").slice(4,));
    });
  
    $(".installation_types").html("");
    $(".categories").html("");
    $(".situations").html("");
    
    $.ajax({
      url: "/get-data-ics",
      type: 'GET',
      success: function(response) {
        response.installation_types.forEach(installation_type => {
          $(".installation_types").append('<option value="'+installation_type.id+'">'+installation_type.name+'</option>');
        });
        $formAddTool.find("#installation_type_id").val("1");
     
        response.categories.forEach(category => {
         $(".categories").append('<option value="'+category.id+'">'+category.name+'</option>');
    	  });
  	    $formAddTool.find("#category_id").val("1");
  	     
        response.situations.forEach(situation => {
         $(".situations").append('<option value="'+situation.id+'">'+situation.name+'</option>');
    	  });
  	   $formAddTool.find("#situation_id").val("1");
  	  }
    });
  });
  
  // Evento de submit que adiciona uma ferramenta
  $formAddTool.on("submit", function(event) {
    event.preventDefault();
    
	  var $button = $modalAddTool.find("[data-btn-add]");
	  var formData = new FormData($formAddTool[0]);
	  var $message = $("#message");
	  
	  $button.attr("disabled", true);
	  $button.text("Aguarde...");
	    
  	$.ajax({
  	  url: "/add-tool",
  	  type: "POST",
  	  data: formData,
  	  processData: false,
  	  contentType: false,
  	  success: function(response) {
  	    $formAddTool[0].reset();
  	    $button.attr("disabled", false);
  	    $button.text("Adicionar");
  	  	$modalAddTool.modal("hide");
  	  	$message.addClass("alert alert-primary");
  	    $message.html(response.msg);
  	  	load_dashboad_tool();
  	  }
  	});
	
  	setTimeout(function() {
      $message.removeClass("alert alert-primary");
      $message.html("");
    }, 5000);
  });
  
  // Evento de clique que visualiza uma ferramenta
  $dashboardContent.on("click", "[data-view-tool-id]", function() {
    var id = $(this).data("view-tool-id");

    $.ajax({
      url: "/view-tool",
      data: {"tool_id": id},
      type: "GET",
      success: function(response) {
        $modalViewTool.find(".modal-body").html(response.view_tool_response);
        $modalViewTool.find("#created").html(moment.utc($modalViewTool.find("#created").html()).fromNow());
        $modalViewTool.find("#modified").html(moment.utc($modalViewTool.find("#modified").html()).fromNow());
      }
    });
  });
  
  // Evento de clique que seleciona uma ferramenta para ser editado
  $dashboardContent.on("click", "[data-edit-tool-id]", function() {
    var tool_id = $(this).data("edit-tool-id");
    var $button = $modalEditTool.find("[data-btn-edit]");
    
    $modalEditTool.find("#link").on("keyup", function() {
  	  $modalEditTool.find("#author").val($modalEditTool.find("#link").val().split("/").slice(3,4));
  	  $modalEditTool.find("#alias").val($modalEditTool.find("#link").val().split("/").slice(4,));
  	  $modalEditTool.find("#name_repo").val($modalEditTool.find("#link").val().split("/").slice(4,));
    });

    $(".installation_types").html("");
    $(".categories").html("");
    $(".situations").html("");

    $.ajax({
      url: "/get-data-tool",
      type: "GET",
      data: {"tool_id": tool_id},
      success: function(response) {
        $(".installation_types").html("");
        $(".categories").html("");
        
        $formEditTool.find("#name").val(response.name);
        $formEditTool.find("#author").val(response.author);
        $formEditTool.find("#alias").val(response.alias);	
        $formEditTool.find("#executable").val(response.executable);
        $formEditTool.find("#name_repo").val(response.name_repo);
        $formEditTool.find("#dependencies").val(response.dependencies);
        $formEditTool.find("#link").val(response.link);
        $formEditTool.find("#installation_tip").val(response.installation_tip);
        $formEditTool.find("#description").val(response.description);
        
	      response.installation_types.forEach(installation_type => {
          $(".installation_types").append('<option value="'+installation_type.id+'">'+installation_type.name+'</option>');
        });
        $formEditTool.find("#installation_type_id").val(response.installation_type_id);

        response.categories.forEach(category => {
	        $(".categories").append('<option value="'+category.id+'">'+category.name+'</option>');
  	    });
  	    $formEditTool.find("#category_id").val(response.category_id);        
  	    response.situations.forEach(situation => {
	        $(".situations").append('<option value="'+situation.id+'">'+situation.name+'</option>');
  	    });
  	    $formEditTool.find("#situation_id").val(response.situation_id);
      }
    });
    
    $button.val(tool_id);
  });
	 
	// Evento de submit que edita uma ferramenta
  $formEditTool.on("submit", function(event) {
    event.preventDefault();
    var $button = $("#modalEditTool [data-btn-edit]");
    var $message = $("#message");
    var formData = new FormData($formEditTool[0]);
    formData.append("tool_id", $button.val());
    
    $button.attr("disabled", true);
    $button.text("Aguarde...");
    
    $.ajax({
  	  url: "/edit-tool",
  	  type: "POST",
  	  data: formData,
  	  processData: false,
  	  contentType: false,
  	  success: function(response) {
  	  	$modalEditTool.modal("hide");
  	  	$button.attr("disabled", false);
  	  	$button.text("Editar");
  	  	$message.addClass("alert alert-warning");
  	    $message.html(response.msg);
  	  	load_dashboad_tool();
  	  }
  	});
  
  	setTimeout(function() {
      $message.removeClass("alert alert-warning");
      $message.html("");
    }, 5000);
  });
  
  // Evento de clique que seleciona uma ferramenta para ser deletada
  $dashboardContent.on("click", "[data-delete-tool-id]", function() {
    var id = $(this).data("delete-tool-id");
    $("[data-btn-delete]").val($(this).data("delete-tool-id"));
  });
  
  // Evento de clique que deleta uma ferramenta
  $modalDeleteTool.find("[data-btn-delete]").on("click", function() {
    var $message = $("#message");
    var $button = $modalDeleteTool.find("[data-btn-delete]");
    
    $.ajax({
      url: "/delete-tool",
      type: "POST",
      data: {"tool_id": $button.val()},
      success: function(response) {
        $modalDeleteTool.modal("hide");
        $message.addClass("alert alert-success");
  	    $message.html(response.msg);
  	  	load_dashboad_tool();
      }
    });
    
    setTimeout(function() {
      $message.removeClass("alert alert-success");
      $message.html("");
    }, 5000);
  });
});
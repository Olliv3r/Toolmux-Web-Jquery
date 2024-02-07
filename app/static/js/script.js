$(document).ready(function() {
  // Carregar ferramentas
  load_tools();
  
  function load_tools() {
    $.ajax({
      url: "/tools",
      type: "GET",
      success: function(response) {
        $("#tableTools").html(response.tools);
      }
    });
  }
  
  // Pesquisa ferramentas no db
  $("#search_text").on("keyup", function() {
    var keyword = $(this).val();
    
    if (keyword !== "") {
      load_search_tools();
    } else {
      load_tools();
    }
  });
  
  // Carrega ferramentas pesquisadas
  function load_search_tools() {
    $.ajax({
      url: "/search-tools",
      type: "GET",
      data: {'keyword': $("#search_text").val()},
      success: function(response) {
        $("#tableTools").html(response.search_tools);
      }
    });
  }
  
  // Paginação
  
  // Anterior
  $("#tableTools").on("click", "[data-page-prev]", function() {
    const page_url = $(this).data("page-prev");
    paginate(page_url);
  });
  
  // Proximo
  $("#tableTools").on("click", "[data-page-next]", function() {
    const page_url = $(this).data("page-next");
    paginate(page_url);
  });
  
  // Paginar
  function paginate(page_url) {
    $.ajax({
      url: page_url,
      type: "GET",
      success: function(response) {
        $("#tableTools").html(response.tools);
      }
    });
  }

  $("#modalAdd #link").on("keyup", function() {
    $("#modalAdd #author").val($("#modalAdd #link").val().split("/").slice(3,4));
    $("#modalAdd #alias").val($("#modalAdd #link").val().split("/").slice(4,));
    $("#modalAdd #name_repo").val($("#modalAdd #link").val().split("/").slice(4,));
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
      $("#add-form #installation_type").val("1");
   
     response.categories.forEach(category => {
       $(".categories").append('<option value="'+category.id+'">'+category.name+'</option>');
  	  });
	     $("#add-form #category").val("1");
	     
     response.situations.forEach(situation => {
       $(".situations").append('<option value="'+situation.id+'">'+situation.name+'</option>');
  	  });
	     $("#add-form #situation").val("1");
	  }
  });
  
  // Adicionar	
  $(".btn-add").on("click", function() {
  	var validated = true;
  	
  	$("#add-form .field").each(function() {
  	  if ($(this).val() === "") {
  	    validated = false;
  	    return;
  	  }
  	});
	  
	  if (validated) {
	    $("#modalAdd .btn-add").attr("disabled", true);
	    var formData = $("#add-form").serialize();
	    
    	$.ajax({
    	  url: "/add-tool",
    	  type: "POST",
    	  data: formData,
    	  success: function(response) {
    	    $("#modalAdd .btn-add").attr("disabled", false);
    	  	$("#modalAdd").modal("hide");
    	  	$("#message").addClass("alert alert-primary");
    	    $("#message").html(response.msg);
    	  	load_tools();
    	  },
    	  error: function(error) {
    	  	console.log('Error: ' + error);
    	  }
    	});
	  }

  	setTimeout(function() {
      $("#message").removeClass("alert alert-primary");
      $("#message").html("");
    }, 5000);
  });
 
  // Visualizar
  $("#tableTools").on("click", "[data-view-tool-id]", function() {
    var id = $(this).data("view-tool-id");

    $.ajax({
      url: "/view-tool",
      data: {"tool_id": id},
      type: "GET",
      success: function(response) {
        $("#modalView .modal-body").html(response.view_tool_response);
      }
    });
  });

  // Editar
  $("#tableTools").on("click", "[data-edit-tool-id]", function() {
    var tool_id = $(this).data("edit-tool-id");

    $("#modalEdit #link").on("keyup", function() {
	  $("#modalEdit #author").val($("#modalEdit #link").val().split("/").slice(3,4));
	  $("#modalEdit #alias").val($("#modalEdit #link").val().split("/").slice(4,));
	  $("#modalEdit #name_repo").val($("#modalEdit #link").val().split("/").slice(4,));
    });

    $(".installation_types").html("");
    $(".categories").html("");
    $(".situations").html("");

    $.ajax({
      url: "/get-data-edit",
      type: "GET",
      data: {"tool_id": tool_id},
      success: function(response) {
        $(".installation_types").html("");
        $(".categories").html("");
        
        $("#edit-form #name").val(response.name);
        $("#edit-form #author").val(response.author);
        $("#edit-form #alias").val(response.alias);	
        $("#edit-form #executable").val(response.executable);
        $("#edit-form #name_repo").val(response.name_repo);
        $("#edit-form #dependencies").val(response.dependencies);
        $("#edit-form #link").val(response.link);
        $("#edit-form #installation_tip").val(response.installation_tip);
        $("#edit-form #description").val(response.description);
        
	      response.installation_types.forEach(installation_type => {
          $(".installation_types").append('<option value="'+installation_type.id+'">'+installation_type.name+'</option>');
        });
        $("#edit-form #installation_type").val(response.installation_type_id);

        response.categories.forEach(category => {
	        $(".categories").append('<option value="'+category.id+'">'+category.name+'</option>');
  	    });
  	    $("#edit-form #category").val(response.category_id);        
  	    response.situations.forEach(situation => {
	        $(".situations").append('<option value="'+situation.id+'">'+situation.name+'</option>');
  	    });
  	    $("#edit-form #situation").val(response.situation_id);
      }
    });
    
    $(".btn-edit").val(tool_id);
  });
	  
  $(".btn-edit").on("click", function() {
    var validated = true;
  	
  	$("#edit-form .field").each(function() {
  	  if ($(this).val() === "") {
  	    validated = false;
  	    return;
  	  }
  	});
    
    if (validated) {
      $.ajax({
    	  url: "/edit-tool",
    	  type: "POST",
    	  data: {
    	    "tool_id": $(".btn-edit").val(),
    	    "name": $("#edit-form #name").val(),
          "author": $("#edit-form #author").val(),
          "alias": $("#edit-form #alias").val(),
          "executable": $("#edit-form #executable").val(),
          "name_repo": $("#edit-form #name_repo").val(),
          "dependencies": $("#edit-form #dependencies").val(),
          "installation_type_id": $("#edit-form #installation_type").val(),
          "link": $("#edit-form #link").val(),
          "installation_tip": $("#edit-form #installation_tip").val(),
          "category_id": $("#edit-form #category").val(),
          "situation_id": $("#edit-form #situation").val(),
          "description": $("#edit-form #description").val()
    	  },
    	  success: function(response) {
    	  	console.log('Sucesso: ', response);
    	  	$("#modalEdit").modal("hide");
    	  	$("#message").addClass("alert alert-warning");
    	    $("#message").html(response.msg);
    	  	load_tools();
    	  },
    	  error: function(error) {
    	  	console.log('Error: ' + error);
    	  }
    	});
    }
    
  	setTimeout(function() {
      $("#message").removeClass("alert alert-warning");
      $("#message").html("");
    }, 5000);
  });


  // Apagar
  $("#tableTools").on("click", "[data-delete-tool-id]", function() {
    var id = $(this).data("delete-tool-id");
    $(".btn-delete").val($(this).data("delete-tool-id"));
  });
  
  $(".btn-delete").on("click", function() {
    $.ajax({
      url: "/delete-tool",
      type: "POST",
      data: {"tool_id": $(".btn-delete").val()},
      success: function(response) {
        $("#modalDelete").modal("hide");
        $("#message").addClass("alert alert-success");
  	    $("#message").html(response.msg);
  	  	load_tools();
      }
    });
    
    setTimeout(function() {
      $("#message").removeClass("alert alert-success");
      $("#message").html("");
    }, 5000);
  });
  
});

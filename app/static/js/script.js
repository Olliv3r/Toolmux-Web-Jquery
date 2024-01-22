// Carregar dados da pesquisa
$(document).ready(function() {
  function load_data(query) {
    $.ajax({
      url: "/data-search",
      method: 'POST',
      data: {query:query}
    }).done(function(response) {
      $("#tools").html(response);
      $("#tools").append(response.responsehtml);
    });
  }

  // Carregar ocorrencias encontradas no DB
  $("#search_text").on("keyup", function() {
    var search = $(this).val();
    
    if (search != '') {
      load_data(search);
    } else {
      get_tools();
    }
  });
});

// Carregar tools
function get_tools() {
  $.ajax({
    url: '/tools',
    dataType: 'json'
  }).done(function(response) {
    $("#tools").html(response.tools_response);
  });
}
get_tools();

// Página anterior e próxima da paginação
$(document).ready(function() {
  $("#tools").on("click", "[data-page-prev]", function() {
    const prev_url = $(this).data('page-prev');

    $.ajax({
      url: prev_url,
      dataType: 'json'
    }).done(function(response) {
      $("#tools").html(response.tools_response);
    });
  });

  $("#tools").on("click", "[data-page-next]", function() {
    const next_url = $(this).data('page-next');

    $.ajax({
      url: next_url,
      dataType: 'json'
    }).done(function(response) {
      $("#tools").html(response.tools_response);
    });
  });
});

// Carregar informaçôes da tool
$(document).ready(function() {
  $("#tools").on("click", "[data-view-tool-id]", function() {
    let tool_id = $(this).data("view-tool-id");
    
    $.ajax({
      url: '/view-tool',
      data: {tool_id: tool_id},
      dataType: 'json'
    }).done(function(response) {
      $("#modalVisualizar .modal-body").html(response.view_tool_response);
    });
  });
});

// Adicionar uma tool
$(document).ready(function() {
  $.ajax({
	url: '/get-data-tc',
	dataType: 'json'
  }).done(function(response) {
    response.types_install.forEach(type_install => {
      $("#modalAdicionar #type_install").append('<option value="' + type_install.id + '">' + type_install.name + '</option>');
    });
    $("#modalAtualizar #type_install").val("1");
    response.categories.forEach(category => {
      $("#modalAdicionar #category").append('<option value="' + category.id + '">' + category.name + '</option>');
    });
    $("#modalAtualizar #category").val("1");	
  });
  
  $("#modalAdicionar").on("click", "[data-save]", function() {
    
    $("#modalAdicionar #add-form").addClass("was-validated");
    
    if ($("#modalAdicionar #name").val() == "") {
      $("#modalAdicionar #name").addClass("is-invalid");
      return;
    } else {
      $("#modalAdicionar #name").addClass("is-valid");
    }
    
    if ($("#modalAdicionar #author").val() == "") {
      $("#modalAdicionar #author").addClass("is-invalid");
      return;
    } else {
      $("#modalAdicionar #author").addClass("is-valid");
    }
      
    if ($("#modalAdicionar #alias").val() == "") {
      $("#modalAdicionar #alias").addClass("is-invalid");
      return;
    } else {
      $("#modalAdicionar #alias").addClass("is-valid");
      $("#modalAdicionar [data-save]").attr("disabled", "");
    }
    
	  $.ajax({
  	  url: '/add-tool',
  	  method: 'POST',
  	  data: {
  	    'name': $("#modalAdicionar #name").val(),
  	    'author': $("#modalAdicionar #author").val(),
  	    'alias': $("#modalAdicionar #alias").val(),
  	    'custom_alias': $("#modalAdicionar #custom_alias").val(),
  	    'name_repo': $("#modalAdicionar #name_repo").val(),
  	    'link': $("#modalAdicionar #link").val(),
  	    'type_install': $("#modalAdicionar #type_install").val(),
  	    'category': $("#modalAdicionar #category").val(),
  	    'dependencies': $("#modalAdicionar #dependencies").val(),
  	    'installation_tip': $("#modalAdicionar #installation_tip").val()
      },
  	  dataType: 'json'
	  }).done(function(response) {
  	  $("#modalAdicionar #add-form").removeClass("was-validated");
  	  $("#message").addClass("alert alert-primary");
  	  $("#message").html(response);
  	  $("#modalAdicionar").modal("hide");
  	  get_tools();
  	});
	
  	setTimeout(function() {
  	  $("#message").removeClass("alert alert-primary");
  	  $("#message").html("");
  	}, 5000);
  });
});

// Atualizar uma tool
$(document).ready(function() {
  $("#tools").on("click", "[data-update-tool-id]", function() {
    let tool_id = $(this).data("update-tool-id");
  	
    $.ajax({
      url: '/get-data-update',
      data: {'tool_id': tool_id},
      dataType: 'json'
    }).done(function(response) {
  	  $("#modalAtualizar #type_install").html("");
  	  $("#modalAtualizar #category").html("");
	  
      $("#modalAtualizar #name").val(response.name);
      $("#modalAtualizar #author").val(response.author);
      $("#modalAtualizar #alias").val(response.alias);
      $("#modalAtualizar #custom_alias").val(response.custom_alias);
      $("#modalAtualizar #name_repo").val(response.name_repo);
      $("#modalAtualizar #link").val(response.link);
      $("#modalAtualizar #dependencies").val(response.dependencies);
      $("#modalAtualizar #installation_tip").val(response.installation_tip);
      
      response.types_install.forEach(type_install => {
        $("#modalAtualizar #type_install").append('<option value="' + type_install.id + '">' + type_install.name + '</option>');
      });
      $("#modalAtualizar #type_install").val(response.type_install_id);
      response.categories.forEach(category => {
        $("#modalAtualizar #category").append('<option value="' + category.id + '">' + category.name + '</option>');
      });
      $("#modalAtualizar #category").val(response.category_id);
      $("#modalAtualizar [data-save]").val(tool_id);
    });
  });
  
  $("#modalAtualizar [data-save]").on("click", function() {
    $("#modalAtualizar #update-form").addClass("was-validated");
    
    if ($("#modalAtualizar #name").val() == "") {
      $("#modalAtualizar #name").addClass("is-invalid");
      return;
    } else {
      $("#modalAtualizar #name").addClass("is-valid");
    }
    
    if ($("#modalAtualizar #author").val() == "") {
      $("#modalAtualizar #author").addClass("is-invalid");
      return;
    } else {
      $("#modalAtualizar #author").addClass("is-valid");
    }
      
    if ($("#modalAtualizar #alias").val() == "") {
      $("#modalAtualizar #alias").addClass("is-invalid");
      return;
    } else {
      $("#modalAtualizar #alias").addClass("is-valid");
    }
    
    $.ajax({
  	  url: '/update-tool',
  	  method: 'POST',
      data: {
  	   'tool_id': $("#modalAtualizar [data-save]").val(),
  	   'name': $("#modalAtualizar #name").val(),
  	   'author': $("#modalAtualizar #author").val(),
  	   'alias': $("#modalAtualizar #alias").val(),
  	   'custom_alias': $("#modalAtualizar #custom_alias").val(),
  	   'name_repo': $("#modalAtualizar #name_repo").val(),
  	   'link': $("#modalAtualizar #link").val(),
  	   'type_install_id': $("#modalAtualizar #type_install").val(),
  	   'category_id': $("#modalAtualizar #category").val(),
  	   'dependencies': $("#modalAtualizar #dependencies").val(),
  	   'installation_tip': $("#modalAtualizar #installation_tip").val()
      },
	    dataType: 'json'
	  }).done(function(response) {
  	  $("#message").addClass("alert alert-primary");
  	  $("#message").html(response.msg);
  	  $("#modalAtualizar").modal("hide");
  	  $("#modalAtualizar #add-form").removeClass("was-validated");
  	  get_tools();
  	}).fail(function(response) {
  	  $("#message").addClass("alert alert-danger");
  	  $("#message").html(response.msg);
  	  $("#modalAtualizar").modal("hide");
      get_tools();
    });
      
    setTimeout(function() {
      $("#message").removeClass("alert alert-danger");
      $("#message").html("");
    }, 5000);
  });
});

// Apagar uma tool
$(document).ready(function() {
  $("#tools").on("click", "[data-delete-tool-id]", function() {
    let tool_id = $(this).data("delete-tool-id");
    
    $("#modalApagar [data-save]").on("click", function() {
      $.ajax({
        url: '/delete-tool',
        method: 'POST',
        data: {'tool_id': tool_id},
        dataType: 'json'
      }).done(function(response) {
        $("#message").addClass("alert alert-primary");
        $("#message").html(response.msg);
        $("#modalApagar").modal("hide");
        get_tools();
      });
    });
    
    setTimeout(function() {
      $("#message").removeClass("alert alert-primary");
      $("#message").html("");
    }, 5000);
  });
});
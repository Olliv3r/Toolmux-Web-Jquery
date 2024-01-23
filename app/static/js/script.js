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
      $("#modalView .modal-body").html(response.view_tool_response);
    });
  });
});

// Adicionar uma tool
$(document).ready(function() {
  $.ajax({
	url: '/get-data-tc',
	dataType: 'json'
	
  }).done(function(response) {
    response.installation_types.forEach(installation_type => {
      $("#modalAdd #installation_type").append('<option value="' + installation_type.id + '">' + installation_type.name + '</option>');
    });
    $("#modalAdd #installation_type").val("1");
    response.categories.forEach(category => {
      $("#modalAdd #category").append('<option value="' + category.id + '">' + category.name + '</option>');
    });
    $("#modalAdd #category").val("1");	
  });
    
  $("#modalAdd").on("click", "[data-save]", function() {
    $("#modalAdd #add-form").addClass("was-validated");
	if ($("#modalAdd #name").val() == "") {
	   $("#modalAdd #name").addClass("is-invalid");
       return;
	} else {
	   $("#modalAds #name").addClass("is-valid");
	}
	       
	if ($("#modalAdd #author").val() == "") {
	   $("#modalAdd #author").addClass("is-invalid");
	   return;
	} else {
	   $("#modalAdd #author").addClass("is-valid");
	}
	         
	if ($("#modalAdd #alias").val() == "") {
	   $("#modalAdd #alias").addClass("is-invalid");
	   return;
	} else {
	   $("#modalAdd #alias").addClass("is-valid");
	}
   
    $.ajax({
      url: '/add-tool',
      method: 'POST',
      data: {
        'name': $("#modalAdd #name").val(),
    	'author': $("#modalAdd #author").val(),
   	    'alias': $("#modalAdd #alias").val(),
  	    'custom_alias': $("#modalAdd #custom_alias").val(),
  	    'name_repo': $("#modalAdd #name_repo").val(),
  	    'link': $("#modalAdd #link").val(),
  	    'installation_type': $("#modalAdd #installation_type").val(),
  	    'category': $("#modalAdd #category").val(),
  	    'dependencies': $("#modalAdd #dependencies").val(),
  	    'installation_tip': $("#modalAdd #installation_tip").val()},
  	  dataType: 'json'
 
    }).done(function(response) {
  	  $("#modalAdd #add-form").removeClass("was-validated");
  	  $("#message").addClass("alert alert-primary");
  	  $("#message").html(response);
  	  $("#modalAdd").modal("hide");
  	  get_tools();
  	});
	
  	setTimeout(function() {
  	  $("#message").removeClass("alert alert-primary");
  	  $("#message").html("");
  	}, 5000);
  });
});

// Editar uma tool
$(document).ready(function() {
  $("#tools").on("click", "[data-edit-tool-id]", function() {
    let tool_id = $(this).data("edit-tool-id");
  	
    $.ajax({
      url: '/get-data-edit',
      data: {'tool_id': tool_id},
      dataType: 'json'
    }).done(function(response) {
  	  $("#modalEdit #installation_type").html("");
  	  $("#modalEdit #category").html("");
	  
      $("#modalEdit #name").val(response.name);
      $("#modalEdit #author").val(response.author);
      $("#modalEdit #alias").val(response.alias);
      $("#modalEdit #custom_alias").val(response.custom_alias);
      $("#modalEdit #name_repo").val(response.name_repo);
      $("#modalEdit #link").val(response.link);
      $("#modalEdit #dependencies").val(response.dependencies);
      $("#modalEdit #installation_tip").val(response.installation_tip);
      
      response.installation_types.forEach(installation_type => {
        $("#modalEdit #installation_type").append('<option value="' + installation_type.id + '">' + installation_type.name + '</option>');
      });
      $("#modalEdit #installation_type").val(response.installation_type_id);
      response.categories.forEach(category => {
        $("#modalEdit #category").append('<option value="' + category.id + '">' + category.name + '</option>');
      });
      $("#modalEdit #category").val(response.category_id);
      $("#modalEdit [data-save]").val(tool_id);
    });
  });
  
  $("#modalEdit [data-save]").on("click", function() {
    $("#modalEdit #edit-form").addClass("was-validated");
    
    if ($("#modalEdit #name").val() == "") {
      $("#modalEdit #name").addClass("is-invalid");
      return;
    } else {
      $("#modalEdit #name").addClass("is-valid");
    }
    
    if ($("#modalEdit #author").val() == "") {
      $("#modalEdit #author").addClass("is-invalid");
      return;
    } else {
      $("#modalEdit #author").addClass("is-valid");
    }
      
    if ($("#modalEdit #alias").val() == "") {
      $("#modalEdit #alias").addClass("is-invalid");
      return;
    } else {
      $("#modalEdit #alias").addClass("is-valid");
    }
    
    $.ajax({
  	  url: '/edit-tool',
  	  method: 'POST',
      data: {
  	   'tool_id': $("#modalEdit [data-save]").val(),
  	   'name': $("#modalEdit #name").val(),
  	   'author': $("#modalEdit #author").val(),
  	   'alias': $("#modalEdit #alias").val(),
  	   'custom_alias': $("#modalEdit #custom_alias").val(),
  	   'name_repo': $("#modalEdit #name_repo").val(),
  	   'link': $("#modalEdit #link").val(),
  	   'installation_type_id': $("#modalEdit #installation_type").val(),
  	   'category_id': $("#modalEdit #category").val(),
  	   'dependencies': $("#modalEdit #dependencies").val(),
  	   'installation_tip': $("#modalEdit #installation_tip").val()
      },
	    dataType: 'json'
	  }).done(function(response) {
  	  $("#message").addClass("alert alert-primary");
  	  $("#message").html(response.msg);
  	  $("#modalEdit").modal("hide");
  	  $("#modalEdit #add-form").removeClass("was-validated");
  	  get_tools();
  	}).fail(function(response) {
  	  $("#message").addClass("alert alert-danger");
  	  $("#message").html(response.msg);
  	  $("#modalEdit").modal("hide");
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
    
    $("#modalDelete [data-save]").on("click", function() {
      $.ajax({
        url: '/delete-tool',
        method: 'POST',
        data: {'tool_id': tool_id},
        dataType: 'json'
      }).done(function(response) {
        $("#message").addClass("alert alert-primary");
        $("#message").html(response.msg);
        $("#modalDelete").modal("hide");
        get_tools();
      });
    });
    
    setTimeout(function() {
      $("#message").removeClass("alert alert-primary");
      $("#message").html("");
    }, 5000);
  });
});

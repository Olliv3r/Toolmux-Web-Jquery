$(document).ready(function() {
  // Carregar comentários
  load_comments();
  
  // Função para carregar comentários
  function load_comments() {
    let default_image = "https://bootdey.com/img/Content/avatar/avatar7.png";
    
    $.ajax({
      url: "/get-comments",
      type: "GET",
      success: function(response) {
        $("#comments").html(response.comments);
        $("#comments #created").html(moment.utc($("#comments #created").html()).fromNow());
        
        if ($("#commentImage").attr("src") == "") {
          $("#commentImage").attr("src", default_image);
        }
        
        
      }
    });
    
  }

  // Eventos de paginação
  $("#comments").on("click", "[data-page-prev], [data-page-next]", function() {
    var page_url = $(this).data("page-prev") || $(this).data("page-next");
    paginate(page_url);
  });
  
  // Função para paginar
  function paginate(page_url) {
    $.ajax({
      url: page_url,
      type: "GET",
      success: function(response) {
        $("#comments").html(response.comments);
        $("#comments #created").html(moment.utc($("#comments #created").html()).fromNow());
      }
    });
  }
  
  // Adicionr comentário
  $(".btn-comment-add").on("click", function(event) {
    event.preventDefault();
    $("#add-comment-form .btn-comment-add").attr("disabled", true);
    $("#add-comment-form .btn-comment-add").text("Aguarde...");
  	var validated = true;
  	
  	$("#add-comment-form .field").each(function() {
  	  if ($(this).val() === "") {
  	    validated = false;
  	    return;
  	  }
  	});
	  
	  if (validated) {
    	$.ajax({
    	  url: "/add-comment",
    	  type: "POST",
    	  data: {"comment": $("#add-comment-form #comment").val()},
    	  success: function(response) {
    	    $("#add-comment-form")[0].reset();
    	    $("#add-comment-form .btn-comment-add").attr("disabled", false);
    	    $("#add-comment-form .btn-comment-add").text("Publicar");
    	  	$("#message").addClass("alert alert-primary");
    	    $("#message").html(response.msg);
    	  	load_comments();
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
  
  // Editar comentário
  $("#comments").on("click", "[data-edit-comment]", function() {
    var comment_id = $(this).data("edit-comment");
    
    $.ajax({
      url: "/get-data-comment",
      type: "GET",
      data: {"comment_id": comment_id},
      success: function(response) {
        $("#editModal .modal-body").html(response.form);
      }
    });
    $(".btn-comment-edit").val(comment_id);
  });
	
  $(".btn-comment-edit").on("click", function() {
    var validated = true;
  	
  	$("#edit-comment-form .field").each(function() {
  	  if ($(this).val() === "") {
  	    validated = false;
  	    return;
  	  }
  	});
    
    if (validated) {
      $(".btn-comment-edit").attr("disabled", true);
      $.ajax({
    	  url: "/edit-comment",
    	  type: "POST",
    	  data: {
    	    "comment_id": $(".btn-comment-edit").val(),
    	    "comment": $("#edit-comment-form #comment").val()
    	  },
    	  success: function(response) {
    	  	$("#editModal").modal("hide");
    	  	$("#message").addClass("alert alert-warning");
    	    $("#message").html(response.msg);
    	  	load_comments();
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

  // Deletar comentário
  $("#comments").on("click", "[data-delete-comment]", function() {
    $(".btn-comment-delete").val($(this).data("delete-comment"));
  });
  
  $(".btn-comment-delete").on("click", function() {
    $.ajax({
      url: "/delete-comment",
      type: "GET",
      data: {"comment_id": $(".btn-comment-delete").val()},
      success: function(response) {
        $("#deleteModal").modal("hide");
        $("#message").addClass("alert alert-success");
  	    $("#message").html(response.msg);
  	  	load_comments();
      }
    });
    
    setTimeout(function() {
      $("#message").removeClass("alert alert-success");
      $("#message").html("");
    }, 5000);
  });
});
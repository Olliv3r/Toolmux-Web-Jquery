function set_message_count(n) {
  $("#message_count").text(m);
  $("#message_count").css("visibility", n ? "visible" : "hidden");
}

$(document).ready(function() {
  var since = 0;
  setInterval(function() {
    $.ajax({
      url: '/notifications?since='+sice,
      type: 'GET',
      success: function(notifications) {
        for (let i = 0; i < notifications.length; i++) {
          if (notifications[i].name == 'unread_message_count') {
            set_message_count(notifications[i].data);
          }
          since = notifications[i].timestamp;
        }
      }
    });
  }, 10000);
  
  $(".btn-message").on('click', function() {
    var validated = true;
    
  	$("send-message-form .field").each(function() {
  	  if ($(this).val() === "") {
  	    validated = false;
  	    return;
  	  }
  	});
	  
	  if (validated) {
	    $.ajax({
	      url: "/send-message",
	      type: 'POST',
	      data: {
	        'recipient': $('#send-message-form #recipient').val(),
	        'message': $('#send-message-form #message').val()
	      },
	      success: function(response) {
	        $("#send-message-form")[0].reset();
	        $("#messageModal").modal("hide");
          $("#message").addClass("alert alert-success");
  	      $("#message").html(response.msg);
	      }
	    });
	  }
	  setTimeout(function() {
      $("#message").removeClass("alert alert-success");
      $("#message").html("");
    }, 5000);
  });
});
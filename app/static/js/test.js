$(document).ready(function() {
  var $image = $("#image");
  var $inputImage = $("#inputImage");
  var $groupButton = $("#groupButton");
  var $cropButton = $("#cropButton");
  var $cancelButton = $("#cancelButton");
  var $saveButton = $("#saveButton");
  var cropData;
  
  $inputImage.on("change", function() {
    var input = this;
    
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function(e) {
        $image.attr("src", e.target.result);

        $image.one("ready", function() {
          $image.cropper("setCropBoxData", {'width': 300, 'height': 300});
          $groupButton.css("display", "block");
          $saveButton.hide();
        });
        
        $image.cropper({
          aspectRatio: 1 / 1,
          crop: function(event) {
            cropData = event.detail;
            console.log(event.detail);
          }
        });
      };
      reader.readAsDataURL(input.files[0]);
    }
  });
  
  $cropButton.on("click", function() {
    $image.cropper("destroy");
    $inputImage.val("");
    $saveButton.show();
    $groupButton.css("display", "none");
  });

  $cancelButton.on("click", function() {
    $image.cropper("destroy");
    $image.attr("src", "");
    $inputImage.val("");
    $groupButton.css("display", "none");
    $saveButton.show();
  });

  $saveButton.on("click", function() {
  	$.ajax({
  	  url: '/save',
  	  type: 'POST',
  	  contentType: 'application/json',
  	  data: JSON.stringify(cropData),
  	  success: function(response) {
  	  	console.log(response.msg);
  	  }
  	});
  });

});
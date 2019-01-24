var API_ENDPOINT = "https://<uniquehash>.execute-api.<aws.region>.amazonaws.com/prod"


function showOpinion() {


	$.ajax({
				url: API_ENDPOINT + '/list',
				type: 'GET',
				success: function (response) {

	        jQuery.each(response, function(i,data) {

						if (data['published'] == true) {
	    					
						$("#opinion").append("<div class='col-lg-12'> \
							<div class='frequent_item'> \
            						<h3>" + data['message'] + "</h3> \
            						<p align='right'>" + data['name'] + ", " + data['firm'] + "</p> \
          						</div> \
        						</div>");

						}


	        });
				},
				error: function () {
						alert("error");
				}
		});
};

document.getElementById("addOpinion").onclick = function(){

	var inputData = {
		"name": $('#postName').val(),
		"firm": $('#postFirm').val(),
		"email" : $('#postEmail').val(),
		"message" : $('#postMessage').val()
	};

	$.ajax({
	      url: API_ENDPOINT + '/sendMail',
	      type: 'POST',
	      data:  JSON.stringify(inputData)  ,
	      contentType: 'application/json; charset=utf-8',
	      success: function (response) {
					document.getElementById("postReturn").textContent="Thank you! Opinion added to database. Publication will be after acceptance adminisrator of this site.";
	      },
	      error: function () {
	          alert("error");
	      }
	  });
};


showOpinion()



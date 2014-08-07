$( "#submit-single" ).on( "click", function ( event ) {
    var userid = document.getElementById("userid").value;
    var bikeid = document.getElementById("bikeid").value;
    var stationid = document.getElementById("stationid").value;
    console.log(window.location.protocol + "//" + window.location.host + "/bike/" + bikeid);    
    window.location.location = window.location.protocol + "//" + window.location.host + "/bike/" + bikeid;
});

$(".row_link").click(function() {
    window.document.location = $(this).attr("href");
});

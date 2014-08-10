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

function update_stats() {
    $.getJSON("http://api.bikeshare.cs.pdx.edu/REST/1.0/stats", function(data) {
        $("#tbikes").html(data['BIKES']);
        $("#tstations").html(data['STATIONS']);
        $("#tbikers").html(data['USERS']);
        $("#abikes").html(data['ACTIVE_BIKES']);
        $("#avgbikes").html(data['BIKES_PER_STATION']); 
    });
}

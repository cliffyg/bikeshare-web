var api_url = "http://api.bikeshare.cs.pdx.edu"

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
    $.getJSON(api_url + "/REST/1.0/stats", function(data) {
        $("#tbikes").html(data['BIKES']);
        $("#tstations").html(data['STATIONS']);
        $("#tbikers").html(data['USERS']);
        $("#abikes").html(data['ACTIVE_BIKES']);
        $("#avgbikes").html(data['BIKES_PER_STATION']); 
    });
}

function check_anomalies() {
    $.getJSON(api_url + "/REST/1.0/anomalies", function(data) {
        if (!$("#anomalies").is(":visible")) {
            $("#anomalies").fadeIn("fast");
        }
        var table = "<table class='table table-striped'>";
        $.each(data['anomalies'], function(i, anomaly) {
            table += "<tr><td>" + anomaly['USER_ID'] + "</td>";
            table += "<td>" + (anomaly['STATUS'] == 1 ? "stolen" : "N/A") + "</td></tr>";
        });
        table += "</table>";
        $("#anomalies-table").html(table);
    })
        .fail(function() {
            if ($("#anomalies").is(":visible")) {
                $("#anomalies").fadeOut("fast");
            }
        });
}

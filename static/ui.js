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
        $("#ptbikes").html(data['PORBIKES']);
        $("#ctbikes").html(data['MITBIKES']);
        $("#tstations").html(data['STATIONS']);
        $("#ptstations").html(data['PORSTATIONS']);
        $("#ctstations").html(data['MITSTATIONS']);
        $("#tbikers").html(data['USERS']);
        $("#ptbikers").html(data['USERS']);
        $("#ctbikers").html('0');
        $("#abikes").html(data['ACTIVE_BIKES']);
        $("#pabikes").html(data['POR_ACTIVE_BIKES']);
        $("#cabikes").html(data['MIT_ACTIVE_BIKES']);
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
            table += "<tr><td>User ID: " + anomaly['USER_ID'] + "</td>";
            table += "<td>Status: " + (anomaly['STATUS'] == 1 ? "Suspicious" : "Suspicious") + "</td></tr>";
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

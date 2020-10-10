let forms = [];
let offices = [];
let estimations = {};

function getEstimations() {
    $.ajax({
        type: "POST",
        url: "/processing",
    }).done(function (data) {
        if (data !== "Error") {
            forms = data[0];
            offices = data[1];
            estimations = data[2];

            for (let i = 0; i < forms.length; i++) {
                if (i == 0) {
                    $("#form").append($("<option selected disabled='disabled'>Select One</option>"));
                }

                let option = $("<option></option>");
                option.val(forms[i][0]);
                option.html(forms[i][0] + " | " + forms[i][1]);
                $("#form").append(option);
            }

            $("#form").on("change", function() {
                let index = 0;
                for (let i = 0; i < forms.length; i++) {
                    if ($("#form").val() === forms[i][0]) {
                        index = i;
                        break
                    }
                }
                
                $("#office").empty();
                for (let i = 0; i < offices[index].length; i++) {
                    if (i == 0) {
                        $("#office").append($("<option selected disabled='disabled'>Select One</option>"));
                    }
                    let option = $("<option></option>");
                    option.val(offices[index][i][0]);
                    option.html(offices[index][i][1]);
                    $("#office").append(option);
                }
                $("#office").attr("disabled", false);
            });

            $("#submit").on("click", function() {
                let estimation = estimations[$("#form").val() + "%21" + $("#office").val()];
                $("#estimationTableBody").empty();
                for (let i = 0; i < estimation[1].length; i++) {
                    let tr = $(""
                        + "<tr><td>" + estimation[1][i][4] + " " + estimation[1][i][5] + " - " + estimation[1][i][6] + " " + estimation[1][i][7] + "</td>"
                        + "<td>" + estimation[1][i][3] + "</td>"
                        + "<td>" + estimation[1][i][1] + "</td>"
                        + "<td>" + estimation[1][i][2] + "</td></tr>");
                        $("#estimationTableBody").append(tr);
                }
                $("#estimationTable").css("display", "block");
                $("#text").css("display", "block"); 
            });
        }
    });
}

$(document).on("ready", getEstimations);
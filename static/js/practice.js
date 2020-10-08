let questions = [];
let count = -1;

function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    while (0 !== currentIndex) {
  
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
}

function getQuestions() {
    $.ajax({
        type: "POST",
        url: "/practice",
    }).done(function (data) {
        if (data !== "Error") {
            questions = data;
            shuffle(questions);            
            $("#submit").on("click", function() {
                if ($('#1').is(':checked')) { 
                    if ($("#answer1").html() === questions[count][1]) {
                        $("#correct").html("Correct.");
                    } else {
                        $("#correct").html('Incorrect. The correct answer is "' + questions[count][1] + '"');
                    }
                    $("#next").css("display", "inline-block");
                    $("#explanation").css("display", "block");
                    $("#explanation").html(questions[count][3]);
                } else if ($('#2').is(':checked')) { 
                    if ($("#answer2").html() === questions[count][1]) {
                        $("#correct").html("Correct.");
                    } else {
                        $("#correct").html('Incorrect. The correct answer is "' + questions[count][1] + '"');
                    }
                    $("#next").css("display", "inline-block");
                    $("#explanation").css("display", "block");
                    $("#explanation").html(questions[count][3]);
                } else if ($('#3').is(':checked')) { 
                    if ($("#answer3").html() === questions[count][1]) {
                        $("#correct").html("Correct.");
                    } else {
                        $("#correct").html('Incorrect. The correct answer is "' + questions[count][1] + '"');
                    }
                    $("#next").css("display", "inline-block");
                    $("#explanation").css("display", "block");
                    $("#explanation").html(questions[count][3]);
                } else if ($('#4').is(':checked')) { 
                    if ($("#answer4").html() === questions[count][1]) {
                        $("#correct").html("Correct.");
                    } else {
                        $("#correct").html('Incorrect. The correct answer is "' + questions[count][1] + '"');
                    }
                    $("#next").css("display", "inline-block");
                    $("#explanation").css("display", "block");
                    $("#explanation").html(questions[count][3]);
                }
            });
            $("#next").on("click", function() {
                count += 1;
                $("#question").html(questions[count][0]);
                $("#answer1").html(questions[count][2][0]);
                $("#answer2").html(questions[count][2][1]);
                $("#answer3").html(questions[count][2][2]);
                $("#answer4").html(questions[count][2][3]);
                $('#1').prop("checked", false);
                $('#2').prop("checked", false);
                $('#3').prop("checked", false);
                $('#4').prop("checked", false);
                $("#correct").html("");
                $("#next").css("display", "none");
                $("#explanation").css("display", "none");
            });
            $("#next").click();
        }
    });
}

$(document).on("ready", getQuestions);
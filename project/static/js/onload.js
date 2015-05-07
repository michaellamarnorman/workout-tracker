$(document).ready(function() {
  var workout_day = document.getElementById("workout-workout").innerHTML;
  var squat = "squat"
  var bench = "bench"
  var row = "row"
  var press = "press"
  var deadlift = "deadlift"
  console.log(workout_day);

  if (workout_day === "A"){
    for(var i = 1; i < 6; i++){
      if (document.getElementById(squat + i).innerHTML !== ""){
        document.getElementById(squat + i).style.background = "red";
      }
      if (document.getElementById(bench + i).innerHTML !== ""){
        document.getElementById(bench + i).style.background = "red";
      }
      if (document.getElementById(row + i).innerHTML !== ""){
        document.getElementById(row + i).style.background = "red";
      }
    }
  }

  if (workout_day === "B"){
    for(var i = 1; i < 6; i++){
      if (document.getElementById(squat + i).innerHTML !== ""){
        document.getElementById(squat + i).style.background = "red";
      }
      if (document.getElementById(press + i).innerHTML !== ""){
        document.getElementById(press + i).style.background = "red";
      }
      if (document.getElementById("deadlift1").innerHTML !== ""){
        document.getElementById("deadlift1").style.background = "red";
      }
    }
  }
});
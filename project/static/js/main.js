 function reps(exercise){
      var x = document.getElementById(exercise);
      if (x.innerHTML === ""){
        x.innerHTML = "5";        
        x.style.background = "red";
      }else if(x.innerHTML === "0"){
        x.innerHTML = "";
        x.style.background = "#d3d3d3";
      }else{
        x.innerHTML = parseInt(x.innerHTML) - 1;
      }
      console.log("clicked!");
      
      var exercise_type = exercise.substring(0, exercise.length - 1);
      var workout_a_or_b = document.getElementById('workout-workout').innerHTML;
      check_sets_complete(exercise_type);

      //var workout_complete = check_if_workout_is_complete();
      //console.log('r : ' + workout_complete);
      
    }

function reps_inp(exercise){
      var x = document.getElementById(exercise);
      if (x.value === ""){
        x.value = "5";        
        x.style.background = "red";
      }else if(x.value === "0"){
        x.value = "";
        x.style.background = "#d3d3d3";
      }else{
        x.value = parseInt(x.value) - 1;
      }
      console.log("clicked!");
      
      var exercise_type = exercise.substring(0, exercise.length - 1);
      
      check_sets_complete(exercise_type);
      var workout_complete = check_if_workout_is_complete();
      console.log('r : ' + workout_complete);
      
    }

    function check_sets_complete(exercise){
      if(exercise === "deadlift"){
        setsComplete = document.getElementById(exercise + "1").innerHTML !== "";
      }else{
        var setsComplete = document.getElementById(exercise + "1").innerHTML !== "" &&
            document.getElementById(exercise + "2").innerHTML !== "" &&
            document.getElementById(exercise + "3").innerHTML !== "" &&
            document.getElementById(exercise + "4").innerHTML !== "" &&
            document.getElementById(exercise + "5").innerHTML !== ""; 
      }
      console.log(setsComplete);
           // document.getElementById('bench-complete').style.display = "inline";
      tO = setTimeout(function label(){
          if(setsComplete){
            var reps_per_set = get_sets_from_html(exercise);
            var weight = document.getElementById(exercise + '-weight').innerHTML + "LB";
            var failed_sets = validate_reps_per_set(reps_per_set);
            if(failed_sets){
              var failed_response = "It's ok to fail.  Try again next workout.";
              document.getElementById(exercise + '-complete').innerHTML = failed_response;
              document.getElementById(exercise + '-complete').style.display = "block";
              
            }else{
            var success_response = "Congrats on "+ weight +" on "+ exercise + "!";
            document.getElementById(exercise + '-complete').innerHTML = success_response;
            document.getElementById(exercise + '-complete').style.display = "block";
            }
            //document.getElementById('bench-complete').innerHTML = "Congrats";
          }else{
            document.getElementById(exercise + '-complete').style.display = 'none';
            
          }
        
        }, 1000);
    }

    function validate_reps_per_set(reps_per_set){
      sets_failed = false
      for(var i = 0; i < reps_per_set.length; i++){
        if(reps_per_set[i] < 5){
          sets_failed = true;
        }
      }

      return sets_failed;
    }

    function get_sets_from_html(exercise_type){
      if (exercise_type === "deadlift"){
        var reps_per_set = [document.getElementById(exercise_type + "1").innerHTML];
      }else{
        var reps_per_set = [
          document.getElementById(exercise_type + "1").innerHTML,
          document.getElementById(exercise_type + "2").innerHTML,
          document.getElementById(exercise_type + "3").innerHTML,
          document.getElementById(exercise_type + "4").innerHTML,
          document.getElementById(exercise_type + "5").innerHTML
        ];
      }
      return reps_per_set;
    }

    function exercise_not_completed(exercise_reps){
      for(var i = 0; i< exercise_reps.length; i++){
        if(exercise_reps[i] === ""){
          return true;
        }
      }
    }

    function check_if_workout_is_complete(){
      var squat = get_sets_from_html("squat");
      var bench = get_sets_from_html("bench");
      var row = get_sets_from_html("row");
      var squats_complete = exercise_not_completed(squat);
      var bench_complete = exercise_not_completed(bench);
      var row_complete = exercise_not_completed(row);
      if(squats_complete || bench_complete || row_complete){
        return false;
      }
      return true;
    }

  function workout_completed(){
    var squat = get_sets_from_html("squat");
    var squats_complete = exercise_not_completed(squat);
    if(document.getElementById("workout-workout").innerHTML === "A"){
      var bench = get_sets_from_html("bench");
      var row = get_sets_from_html("row");
      console.log(row);
      var bench_complete = exercise_not_completed(bench);
      var row_complete = exercise_not_completed(row); 
      var not_complete = squats_complete || bench_complete || row_complete;
      var workout_data = {squat: squat.join(), bench: bench.join(), row: row.join()};
    }
    if(document.getElementById("workout-workout").innerHTML === "B"){
      var press = get_sets_from_html("press");
      var deadlift = get_sets_from_html("deadlift");
      console.log(press);
      var press_complete = exercise_not_completed(press);
      var deadlift_complete = exercise_not_completed(deadlift);
      var not_complete = squats_complete || press_complete || deadlift_complete;
      var workout_data = {squat: squat.join(), press: press.join(), deadlift: deadlift.join()};
    }
    var confirm_complete = false;
    if(not_complete){
      confirm_complete = confirm("All of your sets are not complete, are you sure you want to submit?");
    }else{
      confirm_complete = confirm("Are you ready to submit this workout?");
    }
    
    if(confirm_complete){
      $.ajax({
        method: "POST",
        url: "/save_workout/" + document.getElementById('workout-type').innerHTML,
        data: workout_data
      })
        .success(function( msg ) {
          alert(msg);
          console.log(msg);
        });
      }

}


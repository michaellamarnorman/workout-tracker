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
      
      check_sets_complete(exercise_type);
    }


    function check_sets_complete(exercise){
      
      var setsComplete = document.getElementById(exercise + "1").innerHTML !== "" &&
            document.getElementById(exercise + "2").innerHTML !== "" &&
            document.getElementById(exercise + "3").innerHTML !== "" &&
            document.getElementById(exercise + "4").innerHTML !== "" &&
            document.getElementById(exercise + "5").innerHTML !== ""; 

      console.log(setsComplete);
           // document.getElementById('bench-complete').style.display = "inline";
      tO = setTimeout(function label(){
          if(setsComplete){
            var reps_per_set = get_sets_from_html(exercise);

            var failed_sets = validate_reps_per_set(reps_per_set);
            if(failed_sets){
              var failed_response = "It's ok to fail.  Try again next workout.";
              document.getElementById(exercise + '-complete').innerHTML = failed_response;
              document.getElementById(exercise + '-complete').style.display = "block";
              
            }else{
            var success_response = "Congrats on 125LBs on "+ exercise + "!";
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
      var reps_per_set = [
        document.getElementById(exercise_type + "1").innerHTML,
        document.getElementById(exercise_type + "2").innerHTML,
        document.getElementById(exercise_type + "3").innerHTML,
        document.getElementById(exercise_type + "4").innerHTML,
        document.getElementById(exercise_type + "5").innerHTML
      ]
      
      return reps_per_set
    }

    function workout_complete(){
      var squat = get_sets_from_html("squat");
      var bench = get_sets_from_html("bench");
      var row = get_sets_from_html("row");
      var squats_complete = exercise_not_completed(squat);
      var bench_complete = exercise_not_completed(bench);
      var row_complete = exercise_not_completed(row);
      confirm_complete = false;
      if(squats_complete || bench_complete || row_complete){
        confirm_complete = confirm("All of your sets are not complete, are you sure you want to submit?");
      }else{
        confirm_complete = confirm("Are you ready to submit this workout?");
      }
      if (confirm_complete){
        var msg = "squat: " + squat + "\nbench: " + bench + "\nrow: " + row;
        alert(msg);
      }
    }

    function exercise_not_completed(exercise_reps){
      for(var i = 0; i< exercise_reps.length; i++){
        if(exercise_reps[i] === ""){
          return true;
        }
      }
    }
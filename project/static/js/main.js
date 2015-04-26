 function reps(exercise){
      var x = document.getElementById(exercise);
      if (x.innerHTML === ""){
        x.innerHTML = "5";        
        x.style.background = "red";
      }else if(x.innerHTML === "1"){
        x.innerHTML = "";
        x.style.background = "#d3d3d3";
      }else{
        x.innerHTML = parseInt(x.innerHTML) - 1;
      }
      console.log("clicked");
     
      var tO;
      clearTimeout(tO);
     
      //document.getElementById('bench-complete').style.display = "none";
      var setsComplete = document.getElementById("bench1").innerHTML !== "" &&
            document.getElementById("bench2").innerHTML !== "" &&
            document.getElementById("bench3").innerHTML !== "" &&
            document.getElementById("bench4").innerHTML !== "" &&
            document.getElementById("bench5").innerHTML !== ""; 

      
           // document.getElementById('bench-complete').style.display = "inline";
      tO = setTimeout(function label(){
          if(setsComplete){

            document.getElementById('bench-complete').style.display = "block";
            //document.getElementById('bench-complete').innerHTML = "Congrats";
          }else{
            document.getElementById('bench-complete').style.display = 'none';
            
          }
        
        }, 1500);

      

    }

    function tes(){
      alert('hi');
    }    
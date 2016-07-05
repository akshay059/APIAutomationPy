function loadTestResult(){
  var dd = document.getElementById("files")
  file = dd.value

  var runButton = document.getElementById('runButton')
  runButton.value = "Running tests..."
  runButton.onclick = null
  var xhttp = new XMLHttpRequest()
  xhttp.open("GET", "/adserver/runTest?format=json&file="+file)
  var tBody = document.getElementById("trTable")
  tBody.innerHTML = '';
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4){
          runButton.value = "RUN TESTS"
          runButton.onclick = loadTestResult
        }
        if (xhttp.readyState == 4 && xhttp.status == 200) {
          var data = JSON.parse(xhttp.responseText)
          for (var i = 0; i < data.length - 1 /*last row is counts*/; i++){
            console.log(data[i])
            var r = tBody.insertRow();
            var c = r.insertCell();
            c.innerText = data[i].group;
            c.className = "group" 

            c = r.insertCell();
            c.innerText = data[i].name;
            c.className = "name"  

            c = r.insertCell();
            c.innerText = data[i].response_code;
            c.className = "response_code" 

            c = r.insertCell();
            c.innerText = data[i].passed;
            c.className = "response" + " " + data[i].passed;  

            c = r.insertCell();
            c.className = data[i].passed
            if (data[i].failures){
              c.innerText = data[i].failures;
            }

            if (data[i].step){
              if (c.innerText != "")
                c.innerText = "Step failed : " + c.innerText
              else 
                c.innerText = "Step Passed."
            }
          }
          document.getElementById("passCount").innerText = data[data.length - 1].pass
          document.getElementById("warnCount").innerText = data[data.length - 1].warn
          document.getElementById("failCount").innerText = data[data.length - 1].fail

          document.getElementById("totalCount").innerText = data[data.length - 1].fail + data[data.length - 1].pass + data[data.length - 1].warn + data[data.length - 1].passSteps + data[data.length - 1].warnSteps + data[data.length - 1].failSteps
        } else if (xhttp.readyState == 4){
          if (xhttp.responseText.length < 100)
            alert(xhttp.responseText)
          else{
            alert("some error occurred, please varify if the supplied yaml file and schemas used are syntactically correct.")
          }
        }
      }

  xhttp.send()
}

function loadFiles () {
  var dd = document.getElementById("files")
  dd.innerHTML = ''
  var xhttp = new XMLHttpRequest()
  xhttp.open("GET", "/adserver/getTestFiles?path=test")
  xhttp.onreadystatechange = function() {
    var data = JSON.parse(xhttp.responseText)
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      for (var i = 0; i < data.length; i++){
        var option = document.createElement("option");
        option.text = data[i];
        dd.add(option);
        option.className = "files"
      }
    }
  }
  xhttp.send()
}
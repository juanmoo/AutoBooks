var buget_select = document.getElementById("budget_select");

var opt = document.createElement("option");
opt.value = "budget1";
opt.innerHTML = "budget1";
budget_select.appendChild(opt);

/* Populate Form Elements */

// Get List of Kerberos


const invocation = new XMLHttpRequest();
const url = "http://localhost:5000/users?action=list_all";

function callOtherDomain() {
  if(invocation) {    
    invocation.open('GET', url, true);
    invocation.onreadystatechange = ftn
    invocation.send(); 
  }
}
callOtherDomain();

function ftn() {
  if (invocation.readyState == 4 && invocation.status == 200) {
  
    res = invocation.responseText;
    var obj = JSON.parse(res);
    
    var name_select = document.getElementById("kerberos_select");
    var i = 0;
    for (i = 0; i < obj["names"].length; i++) {
      var name = obj["names"][i];
      var new_opt = document.createElement("option");
      new_opt.innerHTML = name;
      name_select.appendChild(new_opt);
    }
  }
}

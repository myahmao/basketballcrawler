//var ourList = document.getElementById("our-list");
//var ourHeadline = document.getElementById("our-headline");
//var listItems = document.getElementById("our-list").getElementsByTagName("li")

var dropDown = document.getElementById("drop-down");
var textField = document.getElementById("text-field");



//ourButton.addEventListener("click", createNewItem);
//delButton.addEventListener("click", deleteItem);


last = document.getElementsByClassName('text_outputs').length
textoutput='text_output'+last;
          //console.log(textoutput)
element = document.getElementById(textoutput);



/*function createNewItem(){
	//ourList.innerHTML += "<li><textarea rows="+"4"+" cols="+"20"+"> This is test</textarea>something new</li>";

  if(countBox<6) {
  boxNameLast = "text_output"+countBox;
  console.log(boxNameLast)
  countBox++;

  selectName="selete-list"+countBox;
  dropDown.innerHTML += "<select class="+"select-list"+" id="+selectName+"> \
            <option value="+"vpc"+">vpc</option> \
            <option value="+"ethpm"+">ethpm</option> \
            <option value="+"vlan_mgr"+">vlan</option> \
            <option value="+"pvlan"+">pvlan</option> \
            </select>"

  boxName="text_output"+countBox;
  textbox_text = document.getElementById(boxNameLast).value
  
	textField.innerHTML+="<textarea rows="+"10"+" cols="+"30"+" font-size:12px class="+"text_outputs"+" id="+boxName+">"+"{{ data }}"+"</textarea>"
  }


  //"<textarea id='text_output' rows="+"4"+" cols="+"20"+"></textarea>";
}

function deleteItem() {

  last = document.getElementsByClassName('text_outputs').length
  textoutput='text_output'+last;
  console.log("textoutput", textoutput);
  //element = document.getElementById(textoutput);
  if(countBox>0) {
    boxName="text_output"+last;
    document.getElementById(boxName).remove();
    selectName="select-list"+last;
    document.getElementById(selectName).remove();
    countBox--;
  }
}*/

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

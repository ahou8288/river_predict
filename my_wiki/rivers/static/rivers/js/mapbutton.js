function CenterControl(controlDiv, functionList) {
  // Set CSS for the control border.
  var controlUI = document.createElement('div');
  controlUI.style.backgroundColor = '#fff';
  controlUI.style.border = '2px solid #fff';
  controlUI.style.borderRadius = '3px';
  controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
  controlUI.style.cursor = 'pointer';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Click to add a marker to the map';
  controlDiv.appendChild(controlUI);

  var headerText = document.createElement('div');
  headerText.innerHTML = 'Add locations to map';
  controlUI.appendChild(headerText);


  var functionRef;
  var index = 0;
  for (var text in functionList) {
    functionRef = functionList[text];
  // Set CSS for the control interior.
    controlText = document.createElement('span');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.style.paddingBottom = '10px';

    controlText.innerHTML = text;
    controlText.setAttribute('onclick', functionRef+'();');

    controlUI.appendChild(controlText);
    index += 1;
  }
}
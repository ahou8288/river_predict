function CenterControl(controlDiv, functionList) {
    var controlUI = document.createElement('div');
    controlUI.classList.add('controlUI');
    controlUI.title = 'Click to add a marker to the map';
    controlDiv.appendChild(controlUI);

    var headerText = document.createElement('div');
    headerText.innerHTML = 'Add locations to map';
    controlUI.appendChild(headerText);

    var functionRef;

    for (var text in functionList) {
        functionRef = functionList[text];
        controlText = document.createElement('span');
        controlText.classList.add('controlText');

        controlText.innerHTML = text;
        controlText.setAttribute('onclick', functionRef+'();');

        controlUI.appendChild(controlText);

    }
}
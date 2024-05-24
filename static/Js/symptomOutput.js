function toggleInfo(index) {
    index = parseInt(index, 10);
    var infoElement = document.querySelectorAll('.info');
    var div_element = document.getElementById('pred' + index);
    console.log(div_element);
    infoElement.forEach(function (element, i) {
        if (i === index) {
            element.parentElement.classList.add('show');
            var div_element = document.getElementById('pred' + i);
            div_element.classList.add('selected');
        } else {
            element.parentElement.classList.remove('show');
            var div_element = document.getElementById('pred' + i);
            div_element.classList.remove('selected');
        }
    });
}
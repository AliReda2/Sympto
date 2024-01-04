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

function getRandomQuote() {
      var category = 'happiness';
      $.ajax({
          method: 'GET',
          url: 'https://api.api-ninjas.com/v1/quotes?category=' + category,
          headers: { 'X-Api-Key': 'T5gjwYT90I24ZrPU5nUBbA==wbNu9T8q7bv0VJ6T' },
          contentType: 'application/json',
          success: function (result) {
              // Append the quote to the quoteContainer div
              $('#quoteContainer').html('<p>' + '"' + result[0].quote + '"' + '</p>');
          },
          error: function ajaxError(jqXHR) {
              console.error('Error: ', jqXHR.responseText);
          }
      });
  }
  toggleInfo(0)
getRandomQuote();
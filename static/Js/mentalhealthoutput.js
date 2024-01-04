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
getRandomQuote();
$(document).ready(function() {
    $('#type').multiselect({
        includeSelectAllOption: true, // add select all option as usual
        optionClass: function(element) {
            var value = $(element).val();

            if (value%2 == 0) {
                return 'odd'; // reversed
            }
            else {
                return 'even'; // reversed
            }
        }
    });
});
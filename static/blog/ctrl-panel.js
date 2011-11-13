//==============================================================================
// :App:        blog
// :File:       functions
// :Author:     Stuart Cox (stuart.cox@gmail.com)
// :Copyright:  public domain
//==============================================================================

// Initialise when document has loaded
$(document).one('ready', function() {
    // Create handler to prompt user to confirm deletion of posts if 'delete'
    // submit button is pressed
    $('#delete_submit').first().click(function() {
        // Count checked delete boxes and operate accordingly:
        // - if no boxes checked, report this and don't leave this page
        // - if boxes checked, ask for confirmation before submitting (with
        //   good grammar)
        var numChecked = countCheckedBoxes("delete", "delete_form");
        if(numChecked < 1) {
            notify("No posts marked for deletion");
            return false;
        }
        else {
            return reqConfirm("Are you sure you want to delete the selected post" +
                    (numChecked > 1 ? "s" : "") + "?");
        }
    });
});


var Blog = Blog || {};

// Notify user of error/warning; currently just uses an alert box, but could be
// replaced with something better
function notify(msg) {
    alert(msg);
}

// Request confirmation of an action from the user; currently just uses a
// standard confirm box, but could be replaced with something better
function reqConfirm(msg) {
    confirm(msg);
}

// Return the number of checked tickboxes
// Parameters:
// - `name`: name attribute of checkbox set to count checked entries
// - `formId`: (optional) id attribute of the form in which to count checked
//   boxes
function countCheckedBoxes(name, formId) {
    // Select all of the checkbox elements (optionally restricting the query to
    // the defined form)
    var $boxes;
    if(typeof(formId) != "undefined") {
        $boxes = $('#' + formId + ' input[type="checkbox"]');
    }
    else {
        $boxes = $('input[type="checkbox"]');
    }
    // Cycle through checkboxes counting ones which are checked
    var numChecked = 0;
    $boxes.each(function() {
        if($(this).get(0).checked) {
            ++numChecked;
        }
    });
    return numChecked;
}

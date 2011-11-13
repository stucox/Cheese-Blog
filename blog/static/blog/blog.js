//==============================================================================
// :App:        blog
// :File:       blog.js
// :Author:     Stuart Cox (stuart.cox@gmail.com)
// :Copyright:  public domain
//==============================================================================

// Initialise when document has loaded
$(document).one('ready', function() {
    Blog.init($('#content'));
});

// Wrap functions up into a namespace to avoid name clashes (or do nothing if
// it's already been declared)
var Blog = Blog || {};

// Notify user of error/warning; currently just uses an alert box, but could be
// replaced with something better
Blog.notify = function(msg) {
    alert(msg);
};

// Blog.confirm(name, formId)
//
// Request confirmation of an action from the user; currently just uses a
// standard confirm box, but could be replaced with something better
Blog.reqConfirm = function(msg) {
    confirm(msg);
};

// Initialiser for blog pages
Blog.init = function($content) {
    if($content.hasClass("ctrl")) {
        // Create handler to prompt user to confirm deletion of posts if
        // 'delete' submit button is pressed
        $('#delete_submit').click(function() {
            // Count checked delete boxes and operate accordingly:
            // - if no boxes checked, report this and don't leave this page
            // - if boxes checked, ask for confirmation before submitting (with
            //   good grammar)
            var numChecked = Blog.countCheckedBoxes("delete", "delete_form");
            if(numChecked < 1) {
                Blog.notify("No posts marked for deletion");
                return false;
            }
            else {
                return Blog.reqConfirm("Are you sure you want to delete the " +
                        "selected post" + (numChecked > 1 ? "s" : "") + "?");
            }
        });
    }
    if($content.hasClass("edit")) {
        // Turn text areas into tinyMCE WYSIWYG control panes
        tinyMCE.init({
            mode : "textareas",
            theme : "advanced",
            skin : "cheese"
        });
    }
};

// Blog.countCheckedBoxes(name, formId)
//
// Return the number of checked tickboxes
// Parameters:
// - `name`: name attribute of checkbox set to count checked entries
// - `formId`: (optional) id attribute of the form in which to count checked
//   boxes
Blog.countCheckedBoxes = function(name, formId) {
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
};

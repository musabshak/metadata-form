/**
 * This file contains: 
 * - Code for generating the likely URL based off dataset name and short institution name.
 * - Code for the collapsibles denoting the optional checkbox/textbox fields for the dataset page.
 * - Code for navigating between different pages of the form on the client-side.
 * - Code for dynamic rendering of multiple traceset pages.
 * - Code for dynamic rendering of multiple authors.
 */


// ******************* START OF CODE FOR LIKELY URL ******************* //
$('#dset_name').on('input', (e) => {
  let url = $('.likely-URL').html();
  let urlArray = url.split('/');
  urlArray[4]= e.target.value;
  let newUrl = urlArray.join('/');
  $('.likely-URL').html(newUrl);
})

$('#dset_institution_name').on('input', (e) => {
  let url = $('.likely-URL').html();
  let urlArray = url.split('/');
  urlArray[3]= e.target.value;
  let newUrl = urlArray.join('/');
  $('.likely-URL').html(newUrl);
})
// ******************* END OF CODE FOR LIKELY URL ******************* //




// ******************* START OF CODE FOR COLLAPSIBLES ******************* //
var coll = document.getElementsByClassName("show-opt-button");
var i;
for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function(event) {
    event.preventDefault();
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}
// ******************* END OF CODE FOR COLLAPSIBLES ******************* //




// ******************* START OF PAGE NAVIGATION CODE ******************* //
var current_page = 0;
showPage(current_page);

// This function will display the specified page of the form amd fix the 
// next/previous buttons accordingly.
function showPage(n) {
  var x = document.getElementsByClassName("page");
  x[n].style.display = "block";
  if (n == 0) { // Hide previous button if on first page
    $('.prev_button').hide();
  } else {
    $('.prev_button').show();
  }
  if (n == (x.length - 1)) { // Show submit button if on last page
    $('.next_button').html("Submit");
  } else {
    $('.next_button').html('Next <i class="fas fa-arrow-right"></i>');
  }
}

$('.prev_button').html(' Previous <i class="fas fa-arrow-left"></i>');


// This function will figure out which page to display, based on the whether the 
// the user clicked on the 'next' button or the 'previous' button.
function nextPrev(n) {
  var x = document.getElementsByClassName("page");
  
  // Hide the current page:
  x[current_page].style.display = "none";

  // Increase or decrease the current page number by 1:
  current_page = current_page + n;

   // If you have reached the end of the form:
  if (current_page >= x.length) {
    current_page -= 1;
    handleSubmit();
  }

  // Otherwise, display the correct page:
  showPage(current_page);

  // Scroll to the 'next/prev' button part of the page
  let posY = window.scrollY + document.querySelector('#next_button_top').getBoundingClientRect().top;
  window.scroll(0, posY-10); 
}
// ******************* END OF PAGE NAVIGATION CODE ******************* //




// ******************* START OF TRACESET PAGE RENDERING CODE ******************* //

// Read a local text file using synchronous XMLHttp Request
readStringFromFileAtPath = function(pathOfFileToReadFrom) {
  var request = new XMLHttpRequest();
  request.open("GET", pathOfFileToReadFrom, false);
  request.send(null);
  var returnValue = request.responseText;
  return returnValue;
}

// Load the traceset page template
var tsetPageTemplate = readStringFromFileAtPath("templates/trace_page_template_no_value.txt");

// Get the current number of tracesets based on the html that the server has rendered. 
// Update the number of tracesets based on user's input. Render the number of traceset pages the user 
// sees accordingly. 
var currNumTsets;                                    // This is set in the $(document).ready() function at the end of this file
var newNumTsets = 0;
$("#dset_num_tracesets").change(function(event) {    // When user changes number of tracesets ..
  $("#confirm-num-tsets").css("display", "block");   // Show the 'confirm' button
  newNumTsets = parseInt(event.target.value);
  if (newNumTsets < currNumTsets) {
    $('#data-loss-warning').css("display", "block"); // Warn user of data loss if reducing number of tsets
  }
  else {
    $('#data-loss-warning').css("display", "none");
  }
})

$("#confirm-num-tsets").click(function(event) {       // When the 'confirm' button is clicked ..
  if (newNumTsets != 0) {
    $('#data-loss-warning').css("display", "none");   // Hide the warning
    $("#confirm-num-tsets").hide();                   // Hide the 'confirm' button

    /* Render traceset pages according to number of tracesets specified */

    // Increasing num tracesets (just append traceset page template, substituting field names/IDs accordingly)
    if (newNumTsets > currNumTsets) {
      
      for (let i=currNumTsets+1; i<newNumTsets+1; i++) {
        tsetPageTemplateModified = tsetPageTemplate.replace(/\[id\]/g, `${i}`);
        $(".tset-pages").append(tsetPageTemplateModified);
        console.log(i);

        /* Add traceset page validation event handlers for newly created pages */
          
        // Validate required traceset fields
        for (var j = 0; j < tset_required_fields.length; j++) {
          $(`#${tset_required_fields[j].replace('X', i)}`).on('blur', (e) => {validateRequired(e.target.value, e.target.id)});
        }

        // Validate traceset names
        $(`#tset${i}_name`).on('blur', (e) => {validateXsetName(e.target.value, e.target.id)});

        // Validate traceset dates
        $(`#tset${i}_start_date`).on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});
        $(`#tset${i}_end_date`).on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});

        // Also re-attach character limit validation event handlers for newly created pages
        addInputCharLimitValidation();
        addTextAreaCharLimitValidation();
      }
    }

    // Decreasing num tracesets [!! data loss warning]
    else if (newNumTsets < currNumTsets) {
      for (var i=0; i<currNumTsets-newNumTsets; i++) {
        $(".tset-pages").children().last().remove();      // Remove the appropriate number of traceset pages
      }
    }

    currNumTsets = newNumTsets;
    newNumTsets = 0;
  }
})
// ******************* END OF TRACESET PAGE RENDERING CODE ******************* //




// ******************* START OF MULTIPLE AUTHOR RENDERING CODE ******************* //

// Read html template for author details
var authorDetailsTemplate = readStringFromFileAtPath("templates/author_details_template_no_value.txt");

var currNumAuthors;  // This is set in the $(document).ready() function at the end of this file

// Adding one new author
$('#add-author-btn').on('click', (e) => {
  if (currNumAuthors+1 > MAX_AUTHORS) {
    alert("Maximum 4 authors allowed");
    return
  }

  let authorDetailsTemplateModified = authorDetailsTemplate.replace(/\[id\]/g, `${currNumAuthors+1}`);
  $('.author-details').append(authorDetailsTemplateModified);
  currNumAuthors = $('.author-details').children().length;
  $('#dset_num_authors').val(currNumAuthors); // Hidden input field that is used on the server-side for loading form 
                                              // with appropriate number of authors

   // Hide all 'remove author' buttons except for for the last author
   for (var i=2; i<currNumAuthors; i++) {
    $(`.remove-author-btn.author${i}`).hide();
  }

  // Add event handler for the 'remove' button for the new author
  $(`.remove-author-btn.author${currNumAuthors}`).on('click', (e) => {
    const authorID = e.target.offsetParent.classList[1]; // Use offsetParent because click is registered on fa icon, not the underlying button
    $(`div#${authorID}`).remove();
    currNumAuthors = $('.author-details').children().length;
    $(`.remove-author-btn.author${currNumAuthors}`).show();
    $('#dset_num_authors').val(currNumAuthors);
  })
  
  // Add email validation for new author
  $(`#dset_author${currNumAuthors}_email`).on('blur', (e) => {validateEmail(e.target.value, e.target.id)});

  // Re-add input character validation for all input fields (to account for newly created author fields)
  addInputCharLimitValidation();
})
// ******************* END OF MULTIPLE AUTHOR RENDERING CODE ******************* //




// As soon as form is loaded ..
$(document).ready( () => {
  // Find out how many traceset pages and how many authors have been rendered by the server
  currNumTsets = $(".tset-pages").children().length;
  currNumAuthors = $('.author-details').children().length;
  // console.log('current number of tset pages is: ', currNumTsets);

  // Add the 'remove' button event handler for all the authors that have been rendered
  for (var i=2; i<=currNumAuthors; i++) {
    $(`.remove-author-btn.author${i}`).on('click', (e) => {
      const authorID = e.target.offsetParent.classList[1];
      $(`div#${authorID}`).remove();
      currNumAuthors = $('.author-details').children().length;
      $(`.remove-author-btn.author${currNumAuthors}`).show();
      $('#dset_num_authors').val(currNumAuthors);
    })
    $(`.remove-author-btn.author${i}`).hide();
  }

  // Show the remove button only for the last author
  $(`.remove-author-btn.author${currNumAuthors}`).show();

  // Initialize likely URL
  const dsetName = $('#dset_name').val()
  const institutionName = $('#dset_institution_name').val();

  if (institutionName === '') {
    $('.likely-URL').html(`http://crawdad.org/institution-name/${dsetName}`);
  } else {
    $('.likely-URL').html(`http://crawdad.org/${institutionName}/${dsetName}`);
  }
  
})

// Code for Collapsibles
var coll = document.getElementsByClassName("show-opt-button");
var i;

for (i = 0; i < coll.length; i++) {
  // console.log("hey!");
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

var current_page = 0;
showPage(current_page);

function showPage(n) {
  // This function will display the specified page of the form ...
  var x = document.getElementsByClassName("page");
  x[n].style.display = "block";
  // console.log(n);
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    // document.getElementById("prev_button_top").style.display = "none";
    // document.getElementById("prev_button_bottom").style.display = "none";
    $('.prev_button').hide();
  } else {
    // document.getElementById("prev_button_top").style.display = "inline";
    // document.getElementById("prev_button_bottom").style.display = "inline";
    $('.prev_button').show();
  }
  if (n == (x.length - 1)) {
    // document.getElementById("next_button_top").innerHTML = "Submit";
    // document.getElementById("next_button_bottom").innerHTML = "Submit";
    $('.next_button').html("Submit");
  } else {
    // document.getElementById("next_button_top").innerHTML = "Next";
    // document.getElementById("next_button_bottom").innerHTML = "Next";
    $('.next_button').html("Next");
  }
    
}

// This function will figure out which page to display
function nextPrev(n) {
  var x = document.getElementsByClassName("page");
  // console.log(current_page);
  // console.log(x);

  // Hide the current tab:
  x[current_page].style.display = "none";

  // Increase or decrease the current tab by 1:
  current_page = current_page + n;

   // if you have reached the end of the form... :
  if (current_page >= x.length) {
    // alert();
    current_page -= 1;

    handleSubmit();

    //...the form gets submitted:
    //document.getElementById("whole_form").submit();
    //$("#next_button").attr({type:"submit", formaction:"saveprogress.py" })
    // return false;
  }

  // Otherwise, display the correct tab:
  console.log(current_page);
  showPage(current_page);

  // Scroll to the top of the document
  // $(window).scrollTop(0);

  let posY = window.scrollY + document.querySelector('#next_button_top').getBoundingClientRect().top;
  window.scroll(0, posY-10); 

}

// Render Trace Pages

// var tracePageTemplate;
// $.get('other/trace_page_template.txt', function(data) {
//   tracePageTemplate = data;
//   console.log(tracePageTemplate);
// })

// https://wsvincent.com/javascript-array-range-function/
function range(start, edge, step) {
  // If only 1 number passed make it the edge and 0 the start
  if (arguments.length === 1) {
    edge = start;
    start = 0;
  }

  // Validate edge/start
  edge = edge || 0;
  step = step || 1;

  // Create array of numbers, stopping before the edge
  let arr = [];
  for (arr; (edge - start) * step > 0; start += step) {
    arr.push(start);
  }
  return arr;
}

readStringFromFileAtPath = function(pathOfFileToReadFrom) {
  var request = new XMLHttpRequest();
  request.open("GET", pathOfFileToReadFrom, false);
  request.send(null);
  var returnValue = request.responseText;

  return returnValue;
}

// var text = readStringFromFileAtPath( "other/trace_page_template_no_value.txt" );
// console.log(text);

var tsetPageTemplate = readStringFromFileAtPath("templates/trace_page_template_no_value.txt");

var currNumTsets; // default
var newNumTsets = 0;
$("#dset_num_tracesets").change(function(event) {
  $("#confirm-num-tsets").css("display", "block");
  newNumTsets = parseInt(event.target.value);
  if (newNumTsets < currNumTsets) {
    $('#data-loss-warning').css("display", "block");
  }
  else {
    // Warn user of loss of data in last traceset pages
    $('#data-loss-warning').css("display", "none");
  }
})

$("#confirm-num-tsets").click(function(event) {
  if (newNumTsets != 0) {
    $('#data-loss-warning').css("display", "none");
    $("#confirm-num-tsets").hide();
    /* Render traceset pages according to number of tracesets specified */

    // Increasing num tracesets (just append)
    if (newNumTsets > currNumTsets) {
      
      console.log("currnum: ", currNumTsets);
      console.log("newnum: ", newNumTsets);

      // addPage = (i) => {
      //   $.get('other/trace_page_template.txt', (tsetPageTemplate) => {
      //     tsetPageTemplateModified = tsetPageTemplate.replace(/\[id\]/g, `${i}`);
      //     $(".tset-pages").append(tsetPageTemplateModified);
          
      //   });
      //   console.log(`appended ${i}`);
        
      // }

      for (let i=currNumTsets+1; i<newNumTsets+1; i++) {
        tsetPageTemplateModified = tsetPageTemplate.replace(/\[id\]/g, `${i}`);
        $(".tset-pages").append(tsetPageTemplateModified);
        console.log(i);

        /**
          * Traceset pages validation for newly created pages
          */
        for (var j = 0; j < tset_required_fields.length; j++) {
          $(`#${tset_required_fields[j].replace('X', i)}`).on('blur', (e) => {validateRequired(e.target.value, e.target.id)});
        }

        // Validate tracet name
        $(`#tset${i}_name`).on('blur', (e) => {validateXsetName(e.target.value, e.target.id)});

        // Validate traceset dates
        $(`#tset${i}_start_date`).on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});
        $(`#tset${i}_end_date`).on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});

        addInputCharLimitValidation();
        addTextAreaCharLimitValidation();

      }

    }

    // Decreasing num tracesets [!! data loss warning]
    else if (newNumTsets < currNumTsets) {
      for (var i=0; i<currNumTsets-newNumTsets; i++) {
        $(".tset-pages").children().last().remove();
      }
    }

    // If altered numTsets is same as original numTsets, do nothing
    currNumTsets = newNumTsets;
    newNumTsets = 0;
  }
})

var authorDetailsTemplate = readStringFromFileAtPath("templates/author_details_template_no_value.txt");


var currNumAuthors;
$('#add-author-btn').on('click', (e) => {
  if (currNumAuthors+1 > MAX_AUTHORS) {
    alert("Maximum 4 authors allowed");
    return
  }

  let authorDetailsTemplateModified = authorDetailsTemplate.replace(/\[id\]/g, `${currNumAuthors+1}`);
  $('.author-details').append(authorDetailsTemplateModified);
  currNumAuthors = $('.author-details').children().length;
  $('#dset_num_authors').val(currNumAuthors);

   // Hide all 'remove author' buttons except for for the last author
   for (var i=2; i<currNumAuthors; i++) {
    $(`.remove-author-btn.author${i}`).hide();
  }

  $(`.remove-author-btn.author${currNumAuthors}`).on('click', (e) => {
    console.log(e.target.offsetParent);
    const authorID = e.target.offsetParent.classList[1];
    console.log(authorID);
    $(`div#${authorID}`).remove();
    currNumAuthors = $('.author-details').children().length;
    $(`.remove-author-btn.author${currNumAuthors}`).show();
    $('#dset_num_authors').val(currNumAuthors);
  })
  
  for (var i = 1; i <= currNumAuthors; i++) {
    $(`#dset_author${i}_email`).on('blur', (e) => {validateEmail(e.target.value, e.target.id)});
  }
  addInputCharLimitValidation();
})






// // When loading form progress, find out how many traceset pages exist by
// // reading "dset_num_tracesets" value from saved xml file.
// $(document).ready(() => {
//   var xhttp = new XMLHttpRequest();
//   let xml_file_name = getParameterByName('token');
//   console.log(`xml_files/${xml_file_name}.xml`);
//   xhttp.open("GET", `xml_files/${xml_file_name}.xml`, false);
//   xhttp.send();
//   myFunction(xhttp);//(this);
// })

// function myFunction(xml) {
//   var xmlDoc = xml.responseXML;
//   var parser = new DOMParser();
//   var xmlDoc = parser.parseFromString(xml.responseText, "application/xml");
//   var y;
//   y = xmlDoc.getElementsByTagName("dset_num_tracesets");//.childNodes[0];
//   currNumTsets = parseInt(y[0].childNodes[0].nodeValue);
//   console.log(currNumTsets);
//   // alert(y[0].childNodes[0].nodeValue);
// }

// function getParameterByName(name) {
//   var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
//   return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
// }

// When loading form progress, find out how many traceset pages exist
// by finding out the number of children of <div class="tset-pages"> tag.
$(document).ready( () => {
  currNumTsets = $(".tset-pages").children().length;
  currNumAuthors = $('.author-details').children().length;
  console.log('current number of tset pages is: ', currNumTsets);

  for (var i=2; i<currNumAuthors; i++) {
    $(`.remove-author-btn.author${i}`).on('click', (e) => {
      console.log(e.target.offsetParent);
      const authorID = e.target.offsetParent.classList[1];
      console.log(authorID);
      $(`div#${authorID}`).remove();
      currNumAuthors = $('.author-details').children().length;
      $(`.remove-author-btn.author${currNumAuthors}`).show();
      $('#dset_num_authors').val(currNumAuthors);
    })
    $(`.remove-author-btn.author${i}`).hide();
  }

  $(`.remove-author-btn.author${currNumAuthors}`).on('click', (e) => {
    console.log(e.target.offsetParent);
    const authorID = e.target.offsetParent.classList[1];
    console.log(authorID);
    $(`div#${authorID}`).remove();
    currNumAuthors = $('.author-details').children().length;
    $(`.remove-author-btn.author${currNumAuthors}`).show();
    $('#dset_num_authors').val(currNumAuthors);
  })

  
})

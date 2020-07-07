/**
 * This file contains the client-side validation functions. The 'on blur' event listeners are also 
 * attached in this file, as soon as the form is loaded.
 */

 /**
  * Constants
  */

const VALIDATION_ON = true; // client-side validation toggle

// Should match the constants at the top of 'validation_common.py' file
const INPUT_TEXT_CHARLIMIT = 50;
const TEXTAREA_CHARLIMIT = 5000;
const MAX_TSET_PAGES = 15;
const MAX_AUTHORS = 4;

// Required dataset field names
const dset_required_fields = [
  "dset_name", 
  "dset_institution_name",
  "dset_description_short",
  "dset_description_long",
  "dset_num_tracesets",
  "dset_author1_name",
  "dset_author1_email", 
  "dset_author1_institution",
  "dset_author1_country",
  "dset_start_date",
  "dset_end_date"
]

// Required traceset field names
const tset_required_fields = [
  "tsetX_name",
  "tsetX_description_short",
  "tsetX_tech_description",
  "tsetX_start_date",
  "tsetX_end_date"
]

// ******************* END OF CONSTANTS ******************* //

/**
 * Validation Functions
 */

hideError = (selector) => {
  $(selector).removeClass('invalid');
  $(`${selector} ~ .error`).hide();
}

showError = (selector, errorMessage) => {
  $(selector).addClass('invalid');
  $(`${selector} ~ .error`).show();
  $(`${selector} ~ .error`).text( errorMessage || "Something wrong with this field");
}

// Used to validate dataset/traceset names + institution name.
// Only accept alphanumeric characters and '-'
validateXsetName = (value, id) => {
  const XsetName = value;
  const fieldID = `#${id}`;

  const regexp = /^[a-zA-Z0-9-_]+$/;

  hideError(fieldID);

  if (XsetName=== "") {
    const errorMessage = "This is a required field";
    showError(fieldID, errorMessage);
    return false;
  }
  else if (!regexp.test(XsetName)) {
    const errorMessage = "Dataset/Traceset name may contain only alpha-numeric characters, preferably all lowercase";
    showError(fieldID, errorMessage);
    return false;
  } 

  return true;
}

validateNumTsets = (value, id) => {
  const fieldID = `#${id}`;

  hideError(fieldID);

  if (value > MAX_TSET_PAGES) {
    showError(fieldID, `Max can be ${MAX_TSET_PAGES}`);
    $(fieldID).val(MAX_TSET_PAGES);
  }
}

// Validates 'measurement dates' format. Also validates that the start date is <= end date
// for the dataset/traceset.
validateDateFormat = (value, id) => {
  const fieldID = `#${id}`;

  const regexp = /^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$/;

  hideError(fieldID);

  if (value === "") {
    const errorMessage = "This is a required field";
    showError(fieldID, errorMessage);
    return false;
  }
  else if (!regexp.test(value)) {
    console.log('trying to show error', fieldID);
    const errorMessage = "Please make sure date is formatted correctly";
    showError(fieldID, errorMessage);
    return false;
  }

  // If both start and corresponding end dates formatted correctly, 
  // check that start date <= end date.

  // Current event triggered on start date.
  if (/start/.test(fieldID)) {
    const startDateStr = value;
    const temp = fieldID.replace('start', 'end');
    const endDateStr =  $(temp).val();

    hideError(temp);
    if (!regexp.test(endDateStr)) {
      return false;
    }

    const startDateSplit = startDateStr.split('-');
    const endDateStrSplit = endDateStr.split('-');

    const endDate = new Date(endDateStrSplit[0], endDateStrSplit[1]-1, endDateStrSplit[2])
    const startDate = new Date(startDateSplit[0], startDateSplit[1]-1, startDateSplit[2])

    if (endDate < startDate) {
      const errorMessage = "Start date may not be after end date";
      showError(fieldID, errorMessage);
      return false;
    }
  }

  // Current event triggered on end date.
  else if (/end/.test(fieldID)) {
    const endDateStr = value;
    const temp = fieldID.replace('end', 'start');
    const startDateStr =  $(temp).val();

    hideError(temp);
    if (!regexp.test(startDateStr)) {
      return false;
    }

    const startDateSplit = startDateStr.split('-');
    const endDateSplit = endDateStr.split('-');

    const endDate = new Date(endDateSplit[0], endDateSplit[1]-1, endDateSplit[2])
    const startDate = new Date(startDateSplit[0], startDateSplit[1]-1, startDateSplit[2])

    if (endDate < startDate) {
      const errorMessage = "End date may not be before start date";
      showError(fieldID, errorMessage);
      return false;
    }
  }
  return true;
}

validateEmail = (value, id) => {
  const email = value;
  const fieldID = `#${id}`;

  $(fieldID).addClass('email');

  const EMAIL_RE1 = /^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$/;
  const EMAIL_RE2 = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

  hideError(fieldID);

  if (email === "") {
    const errorMessage = "This is a required field";
    showError(fieldID, errorMessage);
    return false;
  }
  else if (!EMAIL_RE1.test(email) || !EMAIL_RE2.test(email)) {
    const errorMessage = "Must provide a correct email";
    showError(fieldID, errorMessage);
    return false;
  } 

  return true;
}

validateInputCharLimit = (value, id) => {
  const inputStr = value;
  const fieldID = `#${id}`;

  if (! ($(fieldID).hasClass('required')) && !($(fieldID).hasClass('email')) ) {
    hideError(fieldID);
  }

  if (inputStr.length > INPUT_TEXT_CHARLIMIT) {
    const errorMessage = `Text must not exceed ${INPUT_TEXT_CHARLIMIT} characters`;
    showError(fieldID, errorMessage);
    return false;
  }

  return true;
}

validateTextAreaCharLimit = (value, id) => {
  const inputStr = value;
  const fieldID = `#${id}`;

  if (! ($(fieldID).hasClass('required')) && !($(fieldID).hasClass('email')) ) {
    hideError(fieldID);
  }

  if (inputStr.length > TEXTAREA_CHARLIMIT) {
    const errorMessage = `Text must not exceed ${TEXTAREA_CHARLIMIT} characters`;
    showError(fieldID, errorMessage);
    return false;
  }

  return true;
}

// Add character limit validation function as the event handler for the 'on blur' event for all
// input[type="text"] fields.
addInputCharLimitValidation = () => {
  const all_text_inputs = $('input[type="text"]').get();
  for (var i=0; i < all_text_inputs.length; i++) {
    $(all_text_inputs[i]).on('blur', (e) => {validateInputCharLimit(e.target.value, e.target.id)});
  }
}

// Add character limit validation function as the event handler for the 'on blur' event for all
// textarea fields.
addTextAreaCharLimitValidation = () => {
  const all_textarea_inputs = $('textarea').get();
  for (var i=0; i < all_textarea_inputs.length; i++) {
    $(all_textarea_inputs[i]).on('blur', (e) => {validateTextAreaCharLimit(e.target.value, e.target.id)});
  }
}

// Event handler for 'required' input fields.
validateRequired = (value, id) => {
  const fieldID = `#${id}`;

  $(fieldID).addClass('required');

  hideError(fieldID);

  if (value === "") {
    const errorMessage = "This is a required field";
    showError(fieldID, errorMessage);
    return false;
  }

  return true;
}

// When saving, only validate the dataset and institution names
validateFormForSave = () => {
  let checks = []

  /* Validate all Xset names*/
  checks.push(validateXsetName($('#dset_name').val(), 'dset_name'));
  checks.push(validateXsetName($('#dset_institution_name').val(), 'dset_institution_name'));
  for (var i=1; i <= currNumTsets; i++) {
    let fieldName = `tset${[i]}_name`;
    let formattedFieldName = `#${fieldName}`;
    checks.push(validateXsetName($(formattedFieldName).val(), fieldName));
  }

  /* Validate all input[type="text"] character limits */
  const all_text_inputs = $('input[type="text"]').get();
  for (var i=0; i < all_text_inputs.length; i++) {
    checks.push(validateInputCharLimit($(all_text_inputs[i]).val(), all_text_inputs[i].id));
  }

  /* Validate all textarea character limits */
  const all_textarea_inputs = $('textarea').get();
  for (var i=0; i < all_textarea_inputs.length; i++) {
    checks.push(validateTextAreaCharLimit($(all_textarea_inputs[i]).val(), all_textarea_inputs[i].id));
  }

  // Return true if every value in 'checks' array is true; false otherwise
  return checks.every((val) => (val===true));
}

validateFormForSubmit = () => {
  let checks = []

  /* Validate all required fields */
  let all_required_fields = dset_required_fields;
  for (var i=1; i <= currNumTsets; i++) {
    for (var j=0; j<tset_required_fields.length; j++) {
      all_required_fields.push(tset_required_fields[j].replace('X', i));
    }
  }
  for (var i=0; i < all_required_fields.length; i++) {
    let formattedField = `#${all_required_fields[i]}`;
    checks.push(validateRequired($(formattedField).val(), all_required_fields[i]));
  }

  /* Validate all Xset names*/
  checks.push(validateXsetName($('#dset_name').val(), 'dset_name'));
  checks.push(validateXsetName($('#dset_institution_name').val(), 'dset_institution_name'));
  for (var i=1; i <= currNumTsets; i++) {
    let fieldName = `tset${[i]}_name`;
    let formattedFieldName = `#${fieldName}`;
    checks.push(validateXsetName($(formattedFieldName).val(), fieldName));
  }

  /* Validate all dates*/
  checks.push(validateDateFormat($('#dset_start_date').val(), 'dset_start_date'));
  checks.push(validateDateFormat($('#dset_end_date').val(), 'dset_end_date'));
  for (var i=1; i <= currNumTsets; i++) {
    let fieldName1 = `tset${[i]}_start_date`;
    let formattedFieldName1 = `#${fieldName1}`;
    let fieldName2 = `tset${[i]}_end_date`;
    let formattedFieldName2 = `#${fieldName2}`;
    checks.push(validateDateFormat($(formattedFieldName1).val(), fieldName1));
    checks.push(validateDateFormat($(formattedFieldName2).val(), fieldName2));
  }

  /* Validate emails*/
  for (var i = 1; i <= currNumAuthors; i++) {
    checks.push(validateEmail($(`#dset_author${i}_email`).val(), `dset_author${i}_email`));
  }

  /* Validate all input[type="text"] character limits */
  const all_text_inputs = $('input[type="text"]').get();
  for (var i=0; i < all_text_inputs.length; i++) {
    checks.push(validateInputCharLimit($(all_text_inputs[i]).val(), all_text_inputs[i].id));
  }

  /* Validate all textarea character limits */
  const all_textarea_inputs = $('textarea').get();
  for (var i=0; i < all_textarea_inputs.length; i++) {
    checks.push(validateTextAreaCharLimit($(all_textarea_inputs[i]).val(), all_textarea_inputs[i].id));
  }

  // Return true if every value in 'checks' array is true; false otherwise
  return checks.every((val) => (val===true));
}


handleSave = (e) => {
  e.stopPropagation();
  const form_valid_for_save = validateFormForSave();

  if (!VALIDATION_ON || form_valid_for_save) {
    $('#whole_form').attr('action', 'progress_save.py');
    $('#whole_form').submit();
  } else {
    $('.save-error').show();
  }
}

handleSubmit = (e) => {
  const form_valid_for_submit = validateFormForSubmit();

  if (!VALIDATION_ON || form_valid_for_submit) {
    $('#whole_form').attr('action', 'progress_submit.py');
    $('#whole_form').submit();
  } else {
    $('.form-error').show();
  }
}

// As soon as document is ready, add validation-performing event handlers to 'on blur' events associated
// with dataset/traceset page input fields.
$(document).ready( () => {
  
  /**
   * Traceset pages validation
   */

  // Add 'required' validation check to relevant traceset fields
  for (var i = 1; i <= currNumTsets; i++) {
    for (var j = 0; j < tset_required_fields.length; j++) {
      $(`#${tset_required_fields[j].replace('X', i)}`).on('blur', (e) => {validateRequired(e.target.value, e.target.id)});
    }

    // Validate traceset name
    $(`#tset${i}_name`).on('blur', (e) => {validateXsetName(e.target.value, e.target.id)});

    // Validate traceset dates
    $(`#tset${i}_start_date`).on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});
    $(`#tset${i}_end_date`).on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});
  }
  
  /**
   * Dataset page validation
   */

  // Add 'required' validation check to relevant dataset fields
  for (var i = 0; i < dset_required_fields.length; i++) {
    $(`#${dset_required_fields[i]}`).on('blur', (e) => {validateRequired(e.target.value, e.target.id)});
  }

  // Validate dataset name
  $('#dset_name').on('blur', (e) => {validateXsetName(e.target.value, e.target.id)});

  // Validate dataset institution name
  $('#dset_institution_name').on('blur', (e) => {validateXsetName(e.target.value, e.target.id)});

  // Validate dataset 'num tracesets'
  $('#dset_num_tracesets').keypress((e) => {e.preventDefault()}); // Prevent typing into number input field
  $('#dset_num_tracesets').on('change', (e) => {validateNumTsets(e.target.value, e.target.id)});
  
  // Validate dataset dates
  $('#dset_start_date').on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});
  $('#dset_end_date').on('blur', (e) => {validateDateFormat(e.target.value, e.target.id)});
  
  // Validate dataset author emails
  for (var i = 1; i <= currNumAuthors; i++) {
    $(`#dset_author${i}_email`).on('blur', (e) => {validateEmail(e.target.value, e.target.id)});
  }

  // Add 'character limit' validation check to all input and textarea fields currently in the form
  addInputCharLimitValidation();
  addTextAreaCharLimitValidation();

  // ******************* END OF VALIDATION ******************* //

  // Attach event handler for "Save Progress" button
  $('#save_progress_button').on('click', handleSave);

  // Attach event handlers for next/prev page buttons
  $('.next_button').on('click', (e) => {e.stopPropagation(); nextPrev(1);});
  $('.prev_button').on('click', (e) => {nextPrev(-1);});

  // Hide error that appears when "Save Progress" is not successful, when user clicks elsewhere
  $('body').not('#save_progress_button').on('click', () => {$('.save-error').hide()});
  
  // Hide error that appears when "Save Progress" is not successful, when user clicks elsewhere
  $('body').not('#next_button_top').on('click', () => {$('.form-error').hide()});

  // If form is navigated to from history (ie browser 'back' button), hard refresh the page. This may happen
  // if a server-side validation check fails and the user presses the 'back' button to go back to the form
  // to fix errors.
  window.addEventListener( "pageshow", function ( event ) {
    var historyTraversal = event.persisted || 
                           ( typeof window.performance != "undefined" && 
                                window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
      // Handle page restore.
      window.location.reload();
    }
  });

})





// $('.error').show();
// $('.error').text("there is some error with this text field!");


/**
 * Validation
 * - All 'textarea' fields have character limit of 5000
 * - All input[type="text"] have character limit of 50
 * - Certain dataset/tracet fields are required
 * - The following fields have special validation checks:
 *    + dset_name
 *    + dset_institution_name
 *    + dset_author1_email
 *    + dset_start_date
 *    + dset_end_date
 *    + tsetX_name
 *    + tsetX_start_date
 *    + tsetX_end_date
 */

const INPUT_TEXT_CHARLIMIT = 50;
const TEXTAREA_CHARLIMIT = 500;
const MAX_TSET_PAGES = 15;

// Required dataset fields
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

// Required traceset fields
const tset_required_fields = [
  "tsetX_name",
  "tsetX_description_short",
  "tsetX_tech_description",
  "tsetX_start_date",
  "tsetX_end_date"
]


/**
 * Validation Methods
 */

hideError = (selector) => {
  $(selector).removeClass('invalid');
  $(`${selector} + .error`).hide();
}

showError = (selector, errorMessage) => {
  $(selector).addClass('invalid');

  $(`${selector} + .error`).show();
  $(`${selector} + .error`).text( errorMessage || "Something wrong with this field");
}

validateXsetName = (e) => {
  const XsetName = e.target.value;
  const fieldID = `#${e.target.id}`;

  const regexp = /^[a-z0-9-]+$/;
  const nameCharLimit = 30;

  hideError(fieldID);

  if (XsetName=== "") {
    const errorMessage = "This is a required field";
    showError(fieldID, errorMessage);
    return false;
  }
  else if (!regexp.test(XsetName)) {
    const errorMessage = "Datset/Traceset name may contain only lowercase alpha-numeric characters ";
    showError(fieldID, errorMessage);
    return false;
  } 

  return true;
}

validateNumTsets = (e) => {
  const fieldID = `#${e.target.id}`;

  // console.log('validating numtsets');

  hideError(fieldID);

  if (e.target.value > MAX_TSET_PAGES) {
    showError(fieldID, `Max can be ${MAX_TSET_PAGES}`);
    $(fieldID).val(MAX_TSET_PAGES);
  }
}

validateDateFormat = (e) => {
  const regexp = /^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$/;

  hideError(`#${e.target.id}`);

  if (e.target.value === "") {
    const errorMessage = "This is a required field";
    showError(`#${e.target.id}`, errorMessage);
    return false;
  }

  else if (!regexp.test(e.target.value)) {
    const errorMessage = "Please make sure date is formatted correctly";
    showError(`#${e.target.id}`, errorMessage);
    return false;
  }

  // If both start and corresponding end dates formatted correctly, 
  // check that start date <= end date

  // Current event triggered on start date
  if (/start/.test(e.target.id)) {
    const startDateStr = e.target.value;
    const temp = `${e.target.id.replace('start', 'end')}`;
    const endDateStr =  $(`#${temp}`).val();

    hideError(`#${temp}`);
    if (!regexp.test(endDateStr)) {
      return true;
    }

    const startDateSplit = startDateStr.split('-');
    const endDateStrSplit = endDateStr.split('-');

    const endDate = new Date(endDateStrSplit[0], endDateStrSplit[1]-1, endDateStrSplit[2])
    const startDate = new Date(startDateSplit[0], startDateSplit[1]-1, startDateSplit[2])

    if (endDate < startDate) {
      const errorMessage = "Start date may not be after end date";
      showError(`#${e.target.id}`, errorMessage);
      return false;
    }
  }

  // Current event triggered on end date
  else if (/end/.test(e.target.id)) {
    const endDateStr = e.target.value;
    const temp = `${e.target.id.replace('end', 'start')}`;
    const startDateStr =  $(`#${temp}`).val();

    hideError(`#${temp}`);
    if (!regexp.test(startDateStr)) {
      return true;
    }

    const startDateSplit = startDateStr.split('-');
    const endDateSplit = endDateStr.split('-');

    const endDate = new Date(endDateSplit[0], endDateSplit[1]-1, endDateSplit[2])
    const startDate = new Date(startDateSplit[0], startDateSplit[1]-1, startDateSplit[2])

    if (endDate < startDate) {
      const errorMessage = "End date may not be before start date";
      showError(`#${e.target.id}`, errorMessage);
      return false;
    }
  }
  return true;
}

validateEmail = (e) => {
  const email = e.target.value;
  const fieldID = `#${e.target.id}`;

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

validateXMLProtection = (e) => {
  let inputString = e.target.value;
  const fieldID = e.target.id;

  inputString = inputString.replace(/&(?!amp;)(?!quot;)(?!apos;)(?!lt;)(?!gt;)/g, '&amp;');
  inputString = inputString.replace(/"/g, '&quot;');
  inputString = inputString.replace(/'/g, '&apos;');
  inputString = inputString.replace(/</g, '&lt;');
  inputString = inputString.replace(/>/g, '&gt;');
  // console.log(inputString);
  // console.log(fieldID);
  $(`#${fieldID}`).val(inputString);
}

// Protect xml for all textarea + input fields
addXMLProtectionValidation = () => {
  const all_text_inputs = $('input[type="text"]').get();
  const all_textarea_inputs = $('textarea').get();
  const all_protectXML_inputs = all_text_inputs.concat(all_textarea_inputs);
  for (var i=0; i < all_protectXML_inputs.length; i++) {
    $(all_protectXML_inputs[i]).on('blur', validateXMLProtection);
    $(all_protectXML_inputs[i]).on('blur', validateXMLProtection);
  }
}

validateInputCharLimit = (e) => {
  const inputStr = e.target.value;
  const fieldID = `#${e.target.id}`;

  // console.log('checking input char limit');

  if (!$(fieldID).hasClass('required')) {
    hideError(fieldID);
  }

  if (inputStr.length > INPUT_TEXT_CHARLIMIT) {
    // console.log('inside if');
    const errorMessage = `Text must not exceed ${INPUT_TEXT_CHARLIMIT} characters`;
    showError(fieldID, errorMessage);
    return false;
  }
}

validateTextAreaCharLimit = (e) => {
  const inputStr = e.target.value;
  const fieldID = `#${e.target.id}`;

  // console.log('checking textarea char limit');

  if (!$(fieldID).hasClass('required')) {
    hideError(fieldID);
  }

  if (inputStr.length > TEXTAREA_CHARLIMIT) {
    // console.log('inside if', fieldID);
    const errorMessage = `Text must not exceed ${TEXTAREA_CHARLIMIT} characters`;
    showError(fieldID, errorMessage);
    return false;
  }
}

addInputCharLimitValidation = () => {
  const all_text_inputs = $('input[type="text"]').get();
  for (var i=0; i < all_text_inputs.length; i++) {
    $(all_text_inputs[i]).on('blur', validateInputCharLimit);
  }
}

addTextAreaCharLimitValidation = () => {
  const all_textarea_inputs = $('textarea').get();
  for (var i=0; i < all_textarea_inputs.length; i++) {
    $(all_textarea_inputs[i]).on('blur', validateTextAreaCharLimit);
  }
}

// "Required" event handler
validateRequired = (e) => {
  // console.log(e.target.value);
  const fieldID = `#${e.target.id}`;

  $(fieldID).addClass('required');

  // console.log('checking textarea required');
  hideError(fieldID);

  if (e.target.value === "") {
    const errorMessage = "This is a required field";
    showError(fieldID, errorMessage);
    return false;
  }

  return true;
}

// As soon as document is ready, add validation-performing event handlers to 'on blur' events associated
// with dataset/traceset page input fields.
$(document).ready( () => {
  /**
   * Tracet pages validation
   */
  for (var i = 1; i <= currNumTsets; i++) {
    // Add 'required' validation check to relevant traceset fields
    for (var j = 0; j < tset_required_fields.length; j++) {
      $(`#${tset_required_fields[j].replace('X', i)}`).on('blur', validateRequired);
    }

    // Validate tracet name
    $(`#tset${i}_name`).on('blur', validateXsetName);

    // Validate traceset dates
    $(`#tset${i}_start_date`).on('blur', validateDateFormat);
    $(`#tset${i}_end_date`).on('blur', validateDateFormat);
  }
  
  /**
   * Dataset page validation
   */

  // Add 'required' validation check to relevant dataset fields
  for (var i = 0; i < dset_required_fields.length; i++) {
    $(`#${dset_required_fields[i]}`).on('blur', validateRequired);
  }

  // Validate dataset name
  $('#dset_name').on('blur', validateXsetName);

  // Validate dataset 'num tracesets'
  $('#dset_num_tracesets').keypress((e) => {e.preventDefault()}); // Prevent typing into number input field
  $('#dset_num_tracesets').on('change', validateNumTsets);
  
  // Validate dataset dates
  $('#dset_start_date').on('blur', validateDateFormat);
  $('#dset_end_date').on('blur', validateDateFormat);
  
  // Validate dataset author email
  $('#dset_author1_email').on('blur', validateEmail);

  // Add 'character limit' validation check to all input and textarea fields currently in the form
  addInputCharLimitValidation();
  addTextAreaCharLimitValidation();
})

handleSubmit = (e) => {
  // const name_valid = validateDatasetName($('#dset_name').val()); 
  // const email_valid = validateEmail($('#dset_author1_email').val());
  // const form_valid = name_valid && email_valid;

  // check all required fields
  // check Xset names
  // check all dates
  // check all emails
  
  if (form_valid) {
    // $('#whole_form').submit();
  } else {
    $('.form-error').show();
  }
}

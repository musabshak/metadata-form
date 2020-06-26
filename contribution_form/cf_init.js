hideError = (selector) => {
  $(selector).removeClass('invalid');
  $(`${selector} + .error`).hide();
}

showError = (selector, errorMessage) => {
  $(selector).addClass('invalid');
  $(`${selector} + .error`).show();
  $(`${selector} + .error`).text( errorMessage || "Something wrong with this field");
}

validateEmail = (email) => {
  const EMAIL_RE1 = /^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$/;
  const EMAIL_RE2 = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

  hideError('#dset_author1_email');

  if (email === "") {
    const errorMessage = "This is a required field";
    showError('#dset_author1_email', errorMessage);
    return false;
  }
  else if (!EMAIL_RE1.test(email) || !EMAIL_RE2.test(email)) {
    const errorMessage = "Must provide a correct email";
    showError('#dset_author1_email', errorMessage);
    return false;
  } 

  return true;
}

validateDatasetName = (datasetName) => {
  const regexp = /^[a-zA-Z0-9-]+$/;
  const nameCharLimit = 30;

  hideError('#dset_name');

  if (datasetName=== "") {
    const errorMessage = "This is a required field";
    showError('#dset_name', errorMessage);
    return false;
  }
  else if (datasetName.length > nameCharLimit) {
    const errorMessage = "Dataset name must not exceed 30 characters";
    showError('#dset_name', errorMessage);
    return false;
  }
  else if (!regexp.test(datasetName)) {
    const errorMessage = "Dataset name may contain only alpha-numeric characters, preferably all lowercase";
    showError('#dset_name', errorMessage);
    return false;
  } 

  return true;
}


handleSubmit = (e) => {
  e.stopPropagation();

  const name_valid = validateDatasetName($('#dset_name').val()); 
  const email_valid = validateEmail($('#dset_author1_email').val());
  const form_valid = name_valid && email_valid;
  
  if (true) {
    $('#whole_form').submit();
  } else {
    $('.form-error.landing-page').show();
  }
}

$('body').not('#submit-button').on('click', () => {$('.form-error.landing-page').hide()});
$('#dset_name').on('blur', (e) => {validateDatasetName(e.target.value)});
$('#dset_author1_email').on('blur', (e) => {validateEmail(e.target.value)});
$('#submit-button').on('click', handleSubmit);



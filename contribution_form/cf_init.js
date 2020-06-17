// var fields = [
//   {
//     name: 'dset_author1_name',
//     display: 'dset_author1_name',
//     rules: 'required|callback_name_len'
//   }
// ]

// function callback(errors, event) {
//   console.log('errors', errors);
//   if (errors.length > 0) {
//     var errorString = '';

//     for (var i = 0, errorLength = errors.length; i < errorLength; i++) {
//       errorString += errors[i].message + ' <br>';
//     }

//     $('.errors').show();
//     $('.errors span').text(errorString);
//   }
// }

// var validator = new FormValidator('whole_form', fields, callback);

// validator.registerCallback('name_len', (value) => {
//   console.log('value', value);
//   if (value.length > 5) {
//     return true;
//   }

//   return false;
// }).setMessage('name_len', "please choose a longer name");


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
  const regexp = /^[a-z0-9-]+$/;
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
    const errorMessage = "Dataset may contain only lowercase alpha-numeric characters ";
    showError('#dset_name', errorMessage);
    return false;
  } 

  return true;
}



handleSubmit = (e) => {

  const name_valid = validateDatasetName($('#dset_name').val()); 
  const email_valid = validateEmail($('#dset_author1_email').val());
  const form_valid = name_valid && email_valid;
  
  if (form_valid) {
    $('#whole_form').submit();
  } else {
    $('#form-error').show();
  }
}

$('#dset_name').on('click', () => $('#form-error').hide());
$('#dset_author1_email').on('click', () => $('#form-error').hide());

$('#dset_name').on('blur', (e) => {validateDatasetName(e.target.value)});
$('#dset_author1_email').on('blur', (e) => {validateEmail(e.target.value)});
$('#submit-button').on('click', handleSubmit);



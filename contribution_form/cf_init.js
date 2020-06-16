const EMAIL_RE1 = /^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$/;
const EMAIL_RE2 = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

validateEmail = (e) => {
  const email = e.target.value;
  $('#dset_author1_email').removeClass('invalid')
  if (email.match(EMAIL_RE1) === null || email.match(EMAIL_RE2) === null ) {
    console.log("One of the two REs not matched")
    $('#dset_author1_email').addClass('invalid')
  }

  // if (email.match(EMAIL_RE2) === null) {
  //   console.log("RE2 not matched")
  // }
}

$('#dset_author1_email').on('blur', validateEmail)
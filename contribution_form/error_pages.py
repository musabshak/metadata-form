SUBMIT_ERROR_PAGE = """
<html>
<head>
  <style>
    body {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Open Sans', sans-serif;
    }

    div#main {
      max-width: 40rem;
    }

  </style>
</head>

<body>
  <div id="main">
    Could not submit form because of the following errors:
    <ul>
      [error_list]
    </ul>
    Please go back to the form by clicking on the back button on your browser and fix the errors.
  </div>
</body>


</html>
"""

SAVE_ERROR_PAGE = """
<html>
<head>
  <style>
    body {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Open Sans', sans-serif;
    }

    div#main {
      max-width: 40rem;
    }

  </style>
</head>

<body>
  <div id="main">
    Could not save form because of the following errors:
    <ul>
      [error_list]
    </ul>
    Please go back to the form by clicking on the back button on your browser and fix the errors.
  </div>
</body>


</html>
"""

SUBMIT_SUCCESS_PAGE = """
<html>
<head>
  <style>
    body {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Open Sans', sans-serif;
    }
    div {
      max-width: 40rem;
    }
  </style>
</head>

<body>
  <div> 
    Thank you for providing metadata to describe your dataset.  
    We will contact you soon if we have any questions or concerns about the details, and to discuss the 
    best means for transfer of your data to our server.
  </div>
</body>

</html>
"""

ALREADY_SUBMITTED_ERROR_PAGE = """
<html>
<head>
  <style>
    body {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Open Sans', sans-serif;
    }
    div#main {
      max-width: 40rem;
    }
  </style>
</head>

<body>
  <div id="main">
    You have already submitted the form; please contact CRAWDAD admin at
    <a target="_blank" href="mailto:crawdad-team@cs.dartmouth.edu">crawdad-team@cs.dartmouth.edu.</a>
    if you wish to make any changes.
  </div>
</body>

</html>
"""
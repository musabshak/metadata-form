# CRAWDAD Metadata Form
This is the metadata form that dataset contributors are requested to fill before uploading a dataset to CRAWDAD. This form 
allows us to collect dataset metadata in a standardized format which we then use to construct a webpage for the uploaded dataset at crawdad.org/

The landing page is accessible at:  
http://home.cs.dartmouth.edu/~crawdad/metadata-form/cf_init.html

You may access forms in progress (not submitted yet) at:  
http://home.cs.dartmouth.edu/~crawdad/metadata-form/progress_load.py?token=yyyy-mm-dd-randomstring-datasetname


## Source Code Structure
_Timeline for when different scripts are called as form is filled_
![](https://i.imgur.com/5srC1kj.jpg)

```cf_init.html```  
New contributors are first pointed to this landing page. The formaction for this static html page is the ```progress_start.py``` script (i.e this page makes a POST request that is processed by the ```progress_start.py``` script). This page contains the following two input fields: 'dataset name' and 'author 1 email'. The dataset name is used to generate the xml file name where the form submission is stored, and the author email is collected because the token URL where the initialized form may be accessed is sent to this email.

```progress_start.py```  
This script takes as input the filled ```cf_init.html``` form as a form object via CGI. It validates the two input fields (server-side). Upon successful validation, an xml tree is generated using the ```xml.etree.ElementTree``` Python library. This tree builds on the ```templates/init.xml``` file that contains all the fieldnames (dataset + first traceset page) as children (with no inner HTML) in the tree at depth 1. The entire xml tree consists of two levels -- depth 0 is the root element "form_in_progress". Depth 1 contains all the form field names. The generated xml tree is then saved to an xml file in the ```xml_files/``` directory. The xml file name follows the following format: ```yyyy-mm-dd-randomstring-datasetname```. The date used is the date when the form was submitted. This script then redirects the contributor to the ```progress_load.py``` script, passing the xml file name as a query parameter in the URL.

```progress_load.py```  
This script renders the form based on the ```templates/cf_template.txt``` file, with the datafield values pre-populated with the saved values in the xml file pointed to by the query parameter 'token' in the URL. Besides the datafield values, there are two structurally major variable elements in the form: the author details and the traceset pages. This script reads the number of authors and the number of traceset pages from the saved xml file and then edits ```templates/cf_template.txt``` accordingly. Subsequently, this script loops through the xml tree in the saved xml file and pre-populates the datafields in the rendered form using string manipulation. That is, the 'value' attribute of the form fields is edited based on the corresponding value in the saved xml file. For example, ```<input type="text" id="dset_name" value=[dset_name]>``` read in from the template would become ```<input type="text" id="dset_name" value="mobility-wireless">```. In the case of textboxes ('textarea' tag in HTML) which do not have a convenient 'value' attribute in HTML, the HTML text of the textboxes is edited. For example, ```<textarea id="dset_description_short">[dset_description_short]</textarea>``` would become ```<textarea id="dset_description_short">This is the saved short description.</textarea>```. So effectively, the 'save progress' functionality is implemented by using string manipulation in Python.

```progress_save.py```  
This script first performs two validation checks on the form: 
- All dataset/traceset names and dataset institution name is formatted correctly?
- All input fields are within the specified character limits?  
These checks are done strictly for security reasons -- the xset names are used to generate directories downstream and it would be undesirable for malicious contributors to be able to specify custom directory names. The character limit checks are also performed as a defense against malicious users.
If the validation checks fail, an error page is rendered. If they succeed, the same xml file generated initially by ```progress_start.py``` is overwritten with the updated progress. This script gets the xml file name from the query parameter of the URL of the previous page. Once the form progress is saved, the contributor is redirected to the ```progress_load.py?token=yyyy-mm-dd-randomstring-datasetname``` script but this time it loads the updated form progress.

```progress_submit.py```  
This script is called when the contributor hits the 'Submit' button at the last page of the form and the client-side validation succeeds. This script first performs the 'validate_for_save' validation checks, to make sure that the form is good to be saved on the server. Once that round of validation passes, the form progress is saved to the xml file. Then the 'validate_for_submit' validation is performed. If those checks are passed, The form progress is saved again, and a notification email is sent to ```crawdadmin@cs.dartmouth.edu``` (updating them about a newly submitted form). If any of the validation checks fail, the user is notified as such and is requested to go back to the form using the browser back button and make the required changes.

```validation_common.py```  
This file contains all the server-side validation functions. The function names mimic those in ```main_validation.js``` -- the file that contains the client-side validation functions.

```error_pages.py```  
This file contains the error/success constant HTML pages that are rendered if there are any validation errors or if the user has successfully submitted the form.

## Form Validation
```main_validation.js```  
The primary form-validation mechanism is client-side; this file contains all the client-side validation code. There are two types of client-side validation checks. The first are validation functions attached to the 'on blur' event for the datafields. That is, once the contributor clicks on a datafield, edits it, and then clicks outside of that field, a quick validation check is performed to ensure that the contributor has not entered invalid input. This ensures that the contributor receives immediate feedback for their input. However, it is possible that the user tries to submit the form without having filled in some required fields, or any field at all, for that matter. To account for that possibility, all the client-side validation checks are performed again once the user presses the 'Submit' button. The form is not allowed to be submitted until the user has fixed all the errors. The errors are highlighted in red.

Of course client-side validation can never be comprehensive because it is happening in-browser and a malicious user may turn these checks off by editing the JS source code in their browser. For that reason, the same validation checks are performed server-side as well. Most of the functions for this server-side validation are contained in the ```validation_common.py``` file. The ```progress_start.py```, ```progress_save.py``` and ```progress_submit.py``` scripts call on these functions as necessary.

__In the case of a non-malicious user, there will never be a case where the form passes the client-side validation but does not pass the server-side validation__. This is because the client and server side validation methods and parameters are identical, save for the syntactical differences due to JS versus Python usage. For this reason, any changes made to the client-side validation parameters must be reflected in the constants in the ```validation_common.py``` script as well

## Editing max authors, max traceset pages, input field character limits
If you wish to change the number of maximum allowed authors, maximum allowed traceset pages, and/or the input field
character limits, you may do so by editing the following constants:
- INPUT_TEXT_CHARLIMIT
- TEXTAREA_CHARLIMIT
- MAX_TSET_PAGES 
- MAX_AUTHORS  
You will have to make sure to edit them in both the following two places: 
- main_validation.js
- validation_common.py

## Other constants/toggles
Form submission check before loading form  
The ```progress_load.py``` script first checks the 'submitted' attribute of the root element of the xml file to make sure that the form has not been submitted. If it has been submitted, the contributor is told that they can no longer access the form and they must contact the CRAWDAD admin for any edits. If it has not been submitted, then the saved form progress is rendered for the contributor. To turn this check off, and display the form regardless of the submittion status, change the ```SUBMIT_CHECK``` constant on top of the ```progress_load.py``` file to ```false```. 

Client-side validation  
If for some reason, you wish to disable the client-side validation, you may turn the ```VALIDATION_ON``` constant on top of the ```main_validation.js``` file to ```false```. 




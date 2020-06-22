import re

file_names = ['contribution_form_template.txt', 'trace_page_template.txt', 'trace_page_template_no_value.txt' ]

for file_name in file_names:

  with open(file_name, 'r') as orig_file:
    orig_file_contents = orig_file.read()
    new_file_contents = re.sub('<label>', '<div>', orig_file_contents)
    new_file_contents = re.sub('<label ', '<div ', new_file_contents)
    new_file_contents = re.sub('</label>', '</div>', new_file_contents)
    with open(file_name.replace('.txt', '1.txt'), 'w') as new_file:
      print(new_file_contents, file=new_file)



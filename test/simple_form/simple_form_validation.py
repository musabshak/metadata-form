#!/usr/bin/python
import cgi,cgitb

print("Content-Type:text/html\n")                          
 
cgitb.enable() #for debugging
form = cgi.FieldStorage()

print(", ".join(form.getlist("hair color")))
cgi.print_form(form)
cgi.print_directory()
print(form.keys())

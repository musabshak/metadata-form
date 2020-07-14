from email.message import EmailMessage
import smtplib, ssl

def email_token(receiver_email, token):
  """
  Send token link to author for accessing the initialized metadata form.
  """
  ## Setting up server and credentials
  # port = 465  # For SSL
  # smtp_server = "smtp.gmail.com"
  # sender_email = "emailtesting253@gmail.com"  
  # password = "emailtesting123"

  # port = 587
  smtp_server = "mail.cs.dartmouth.edu"
  sender_email = "mshakeel@cs.dartmouth.edu"
  # password = "oD/vx0y.cr5j"

  ## Set up message content
  message = EmailMessage()
  message['Subject'] = "Contribution Form Token"
  # message['From'] = f"CRAWDAD {sender_email}"
  # message['To'] = receiver_email
  content = f"You may access the contribution form you started at the " \
  f"following link:\n\n{token}.\n\nReply-to: crawdad-team@cs.dartmouth.edu"
  message.set_content(content)

  server = smtplib.SMTP(smtp_server)
  server.send_message(message, from_addr=sender_email, to_addrs=receiver_email)

  # context = ssl.create_default_context()
  # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
  #     server.login(sender_email, password)
  #     server.send_message(message)


submit_email_notification('hi@sdfsdf')
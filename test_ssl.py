import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
print("SSL works!")
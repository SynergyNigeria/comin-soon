import smtplib
server = smtplib.SMTP('smtp.zoho.com', 587)
server.starttls()
print("SSL works!")
import smtplib
from Gku import settings

def sendMail(fromAddr, to, cc, subject, message, smtpServer='smtp.gmail.com:587'):
    header = "From: {0}To: {1}Cc: {2}Subject: {3}".format(fromAddr, ','.join(to), ','.join(cc), subject)
    message += header
    login = fromAddr.split('@')[0]

    server = smtplib.SMTP(smtpServer)
    server.starttls()
    server.login(fromAddr, settings.EMAIL_HOST_USERS[fromAddr])
    print(login)
    print(settings.EMAIL_HOST_USERS[fromAddr])
    problems = server.sendmail(fromAddr, to, message)
    server.quit()

    return problems
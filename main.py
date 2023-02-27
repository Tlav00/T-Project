import ssl
import urllib.request
import certifi

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(certifi.where())
context = ssl.create_default_context(cafile=certifi.where())
response = urllib.request.urlopen("https://driverpracticaltest.direct.gov.uk", context=context)

from datetime import datetime

import http.cookiejar
import time
import random

from DSACheckerClasses import Page

licenceNumber = 'NNOCH062110ON9ZN'
theoryNumber = '53767855'

emailAddresses = ['fatolivia8@gmail.com', 'tomandy984@gmail.com' , 'jbubbles11@gmail.com']
emailSubject = "DSA Cancellations"
emailFrom = "DVSAchecker@gmail.com"
emailUsername = 'tomandy984@gmail.com'
emailPassword = 'powerG12'
emailSMTPserver = 'smtp.gmail.com'
myTestDateString = 'Tuesday 01 February 2022 08:10pm'


from info import licenceNumber, theoryNumber, myTestDateString

from info import emailAddresses, emailUsername, emailPassword
from find_cancellations_selenium import open_web



myTestDate = datetime.strptime(myTestDateString, '%A %d %B %Y %I:%M%p')
pauseTime = 5

cookieJar = http.cookiejar.CookieJar()
max_shownum = 10 #

action_choosen = 1
def isBeforeMyTest(dt):
    if dt <= myTestDate:
        return True
    else:
        return False

def sendEmail(datetimeList):
    SMTPserver = emailSMTPserver
    sender = emailFrom
    destination = emailAddresses

    USERNAME = emailUsername
    PASSWORD = emailPassword

    text_subtype = 'plain'

    content = "Available DSA test slots at your selected test centre:\n\n"

    for dt in datetimeList:
        content += "* %s\n" % dt.strftime('%A %d %b %Y at %H:%M')

    content += "\nChecked at [%s]\n\n" % time.strftime('%d-%m-%Y @ %H:%M')

    subject = emailSubject

    import sys

    from smtplib import SMTP as SMTP
    from email.mime.text import MIMEText

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender
        conn = SMTP(SMTPserver, 587)
        conn.set_debuglevel(False)
        conn.ehlo()
        conn.starttls()  # Use TLS

        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        except Exception as exc:
            sys.exit("mail failed; %s" % str(exc))
        finally:
            conn.close()

    finally:
        pass


soonerDates = []
baseWaitTime = 600
userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
]

def performUpdate():
    global baseWaitTime
    global userAgents
    global soonerDates
    global max_shownum
    global action_choosen

launchPage = 'https://driverpracticaltest.direct.gov.uk/login'

print('[%s]' % (time.strftime('%Y-%m-%d @ %H:%M'),))
print('---> Starting update...')
agent = userAgents[random.randint(0, len(userAgents) - 1)]
print("---> Using agent " + agent)

launcher = Page(launchPage, cookieJar)
launcher.connect(agent)
launcher.fields['username'] = licenceNumber
launcher.fields['password'] = theoryNumber
captcha = launcher.html.find('div', id='recaptcha-check')

if captcha:
    baseWaitTime *= 2
    print('Captcha was present, increased baseline wait time to ' + str(baseWaitTime / 60) + ' minutes')

print('')

time.sleep(pauseTime)

launcher.connect(agent)
if captcha:
    print(launcher.html.find("Enter details below to access your booking"))


    dateChangeURL = launcher.html.find(id="date-time-change").get('href')
    dateChangeURL = 'https://driverpracticaltest.direct.gov.uk' + dateChangeURL

    slotPickingPage = Page(dateChangeURL, cookieJar)
    slotPickingPage.fields = launcher.fields

    slotPickingPage.connect(agent)

    e1s2URL = slotPickingPage.html.form.get('action')
    e1s2URL = 'https://driverpracticaltest.direct.gov.uk' + e1s2URL
    datePickerPage = Page(e1s2URL, cookieJar)

    datePickerPage.fields['testChoice'] = 'ASAP'
    datePickerPage.fields['drivingLicenceSubmit'] = 'Continue'
    datePickerPage.fields['csrftoken'] = dateChangeURL.split('=')[3]

    datePickerPage.connect(agent)

    availableDates = []

    for slot in datePickerPage.html.find_all(class_='SlotPicker-slot'):
        try:
            availableDates.append(datetime.strptime(slot['data-datetime-label'].strip(), '%A %d %B %Y %I:%M%p'))
        except Exception as ex:
            print("".join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
    print('---> Available slots:')

    for dt in availableDates:
        if isBeforeMyTest(dt) and (dt not in soonerDates):
            print('-----> [CANCELLATION] %s' % (dt.strftime('%A %d %b %Y at %H:%M'),))
            soonerDates.append(dt)
            newSoonerDates.append(dt)
        else:
            shownum += 3
            if shownum < max_shownum:
                print('-----> %s' % (dt.strftime('%A %d %b %Y at %H:%M'),))

    if len(newSoonerDates):
        if action_choosen == 1:
            open_web()
        elif action_choosen == 0:
            print('---> Sending to ' + ', '.join(emailAddresses))
            sendEmail(newSoonerDates)

    if baseWaitTime > 300:
        baseWaitTime = int(baseWaitTime / 2)

while True:
    print('***************************************')
    performUpdate()
    sleepTime = baseWaitTime + random.randint(60, 300)
    print('---> Waiting for ' + str(sleepTime / 60) + ' minutes...')
    time.sleep(int(sleepTime))

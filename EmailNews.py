#!/usr/bin/python

# title: CUFE - CHS EmailNews
# author: Mazen Amr

# gets latest news from the college website
# and sends it to students via email

import chardet, email, os, smtplib, sys, time, urllib3
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

starttime = time.time()
URL = "http://eng.cu.edu.eg/en/credit-hour-system/"
EMAIL = ""
PASSWORD = ""
EMAIL_LIST = ""


def main():
    pretime = time.time()
    page = getpage(URL)
    date, title, link = getinfo(page)
    date = date[8:16] + date[-3:-1]
    loadtime = time.time() - pretime
    runtime = round(time.time() - starttime)
    os.system("clear")
    try:
        open("history", 'r')
    except FileNotFoundError:
        open("history", 'w+')
    if [date, title] not in [line[:-1].split(':') for line in open("history")]:
        open("history", 'a+').write("{}:{}\n".format(date, title))
        newupdate(title, link, date)
    print("Latest News: {}".format(title))
    print("Date: {}".format(date))
    print("Link: {}".format(link))
    print("Loading Time: {0:.2f} seconds".format(loadtime))
    print("Runtime: {}:{}:{}".format\
      (runtime // 3600, (runtime % 3600) // 60, runtime % 3600 % 60))
    time.sleep(3)
    main()


def getpage(url):
    page = urllib3.PoolManager().request('GET', url).data
    return page.decode(chardet.detect(page)['encoding'])


def getinfo(page):
    location = page.find("الإعلانات العامة لبرامج الساعات المعتمدة")
    location = page.find("center", location)
    date = page[location: page.find("/strong", location)]
    location = page.find("24pt", location)
    title = page[location + 6:page.find('<', location)]
    location = page.find("href", location)
    link = page[location + 6:page.find('>', location) - 1]
    return date, title, link


def newupdate(title, link, date):
    os.system("clear")
    print("New update found!")
    print("Sending emails...")
    pdf = MIMEBase('application', 'pdf')
    pdf.set_payload(urllib3.PoolManager().request('GET', link).data)
    email.encoders.encode_base64(pdf)
    pdf.add_header\
      ('Content-Disposition', 'attachment', filename="{}.pdf".format(title))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL, PASSWORD)
    for e in [email[:-1].split(':') for email in open(EMAIL_LIST)]:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = e[1]
        msg['Subject'] = "CUFE Update: {}".format(title)
        msg.attach(MIMEText("Dear {},\n\tNew updates have been added to CUFE - CHS official website (http://eng.cu.edu.eg/en/credit-hour-system) on {}.".format(e[0], date)))
        msg.attach(pdf)
        server.send_message(msg)
    server.quit()
    print("Done!")
    time.sleep(3)
    os.system("clear")


def exit():
    try:
        if input("\nDo you want to exit? [Yn]\n").lower() != 'n':
            sys.exit(0)
        else:
            main()
    except (KeyboardInterrupt, EOFError) as error:
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError) as error:
        exit()

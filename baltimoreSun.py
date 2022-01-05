import requests
from bs4 import BeautifulSoup
import smtplib


def get_links():  # function grabs the links and appends to a list
    balitmore_sun = "https://www.baltimoresun.com/"
    r_baltimore = requests.get(balitmore_sun)  # attain the urls
    soup = BeautifulSoup(r_baltimore.text, "html.parser")

    urls = []
    for link in soup.findAll("a", {"class", "no-u"}):  # find all the urls
        urls.append(balitmore_sun + link.get("href"))  # only the end parts are in the html need to add balitmore sun
    return urls


def text_from_urls(urls):
    for i in range(1):
        idk = requests.get(urls[i])

        html_file = BeautifulSoup(idk.content, "html.parser")
        # take title, author, date, body of text

        # title of the article
        title = html_file.findAll("h1")
        actual_title = title[0].text

        # author of the article
        author = html_file.findAll("span",
                                   {"class:",
                                    "uppercase"})  # trying to find the authors name by narrowing in on the class
        authors_name = author[0].text  # convert to text

        date = html_file.findAll("span", {"class", "timestamp timestamp-article"})
        actual_date = date[1].text

        # body
        body = html_file.findAll("p", {"class", ""})
        final = [actual_title, authors_name + "," + actual_date]
        for x in range(len(body)):
            final.append(body[x].text)

        final_string = ""
        for i in range(len(final)):
            final_string += "{}\r\n".format(final[i])
        return final_string


def email_sender(final_string):     # not secure at all just to test.
    user_gmail = input("What is your gmail? ")        
    password_gmail = input("What is your password? ")
    sender_email = input("Whom do you want to send this to? ")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(user_gmail, password_gmail)
        subject = "Baltimore Sun Top News"

        email_body = f"Subject: {subject}\n\n{final_string})"
        smtp.sendmail(user_gmail, sender_email, email_body)


email_sender(text_from_urls(get_links()))

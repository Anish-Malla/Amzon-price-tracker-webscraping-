import bs4
import urllib.request
import time
import smtplib
import pandas as pd
from datetime import datetime

url = 'https://www.amazon.in/FancyDressWale-Halloween-Inflatable-Tyrannosaurus-Performance/dp/B085RGBGLC/ref=sr_1_1?crid=345OCY4THDAGE&dchild=1&keywords=dinosaur+costume&qid=1593953482&sprefix=dinaosa%2Caps%2C266&sr=8-1'
sauce = urllib.request.urlopen(url).read()
soup = bs4.BeautifulSoup(sauce, "html.parser")
print(soup)

price_list = []

df = pd.DataFrame(columns=["Time", "Price"])

def price_decrease(price_list):
    if price_list[-1] > price_list[-2]:
        return False
    else:
        return True

def email(email_id, text):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("anishtesting1234@gmail.com", "Welcome123#ismypassword")
    s.sendmail("anishtesting1234@gmail.com", email_id, text)
    s.quit()

count = 0
while True:
    price = soup.find(id="priceblock_ourprice")
    price = price.get_text()
    price = float(price.replace(',', '').replace('₹', ''))
    print(price)

    if count >= 0 or price != price_list[-1]:
        price_list.append(price)

        df = df.append({"Time": datetime.now(), "Price": price}, ignore_index=True)
        df.to_csv("price_list.csv")
        if count >= 0:
            if price_decrease(price_list):
                print("THE PRICE WENT DOWN")
                # print(text)
                dif = price_list[-2] - price_list[-1]
                message = f"PRICE WENT DOWN BY {dif} rupees. BUY NOW!"
                # message = "HI MY NAME IS ANISH U DOG 123343"
                email('mallasaianish@gmail.com', message)
                print("sent")

            else:
                print("THE PRICE WENT UP")

    count += 1

    # time.sleep(21600)
    time.sleep(10)

# send_email(price_list, 'mallasaianish@gmail.com')

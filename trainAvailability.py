# from requests_html import HTMLSession
# from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import date


# session = HTMLSession()
# respons = session.get().html


class CheckingBot():

    def __init__(self, train_number, date, class_):
        self.train_number = train_number
        self.driver = webdriver.Firefox()
        self.date = date
        self.class_ = class_

    def checkConnection(self):
        driver = self.driver
        train_number = self.train_number

        try:
            driver.get(
                f'https://www.trainman.in/seat-availability/{train_number}')
            return True
        except:
            return False

    def checkAvailability(self):
        date = self.date
        class_ = self.class_
        driver = self.driver

        dates = driver.find_element_by_xpath(
            f'//tbody/tr[{date}]/td[{class_}]')
        dates.click()

        for _ in range(10):
            dates = driver.find_element_by_xpath(
                f'//tbody/tr[{date}]/td[{class_}]').text
            if dates[-4:] == 'Book':
                break
            time.sleep(2)

        info = []
        for i in range(6):
            availability = driver.find_element_by_xpath(
                f'//tbody/tr[{date - 2 + i}]/td[{class_}]').text
            try:
                slash_n = [i for i, x in enumerate(availability) if x == '\n']
                info.append((
                    availability[:slash_n[0]], 'Probablity : '+availability[slash_n[0] + 1:slash_n[1]]))
            except:
                info.append('Cannot Check')

        return info

    def closeBrowser(self):
        self.driver.close()


def takeInput():

    try:
        # Taking Input of Train Number.
        train_number = int(input('Enter the Train Number : '))

        # Taking Input of travelling date and calculating the total number of days between travelling date and current date.
        travel_date, travel_month = [int(x) for x in input(
            'Enter the Preferred Date in the format dd/mm: ').split('/')]
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        today_date, this_month = [int(x)
                                  for x in date.today().strftime("%d/%m").split('/')]
        total_days = travel_date - today_date + 1
        for month_day in month_days[this_month - 1:travel_month - 1]:
            total_days += month_day

        # Taking input of preferred class.
        class_ = input('Enter Any one  Class "2A 3A SL": ').lower()
        classes = {'2a': 2, '3a': 3, 'sl': 4}
        class_ = classes[class_]

        return train_number, total_days, class_, travel_date, travel_month
    except:
        print('\nIncorrect data\nTry Again\n')
        train_number, total_days, class_ = takeInput()
        return train_number, total_days, class_


if __name__ == "__main__":

    # Calling takeInput function to take Inputs without any Errors.
    train_number, total_days, class_, travel_date, travel_month = takeInput()

    # Creating Object of CheckingBot and Establishing Connection.
    checking = CheckingBot(train_number, total_days, class_)
    print("Waiting for the serve's response...")
    status = checking.checkConnection()
    if status:
        print('Connection Established')
        info = checking.checkAvailability()
        print('Date\tAvailability')
        [print(f'{travel_date - 2 + x}/{travel_month}\t{info[x]}')
         for x in range(6)]
        checking.closeBrowser()
    else:
        print('Server not Responding')
        checking.closeBrowser()

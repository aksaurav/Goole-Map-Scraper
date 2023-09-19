"""Part 1: Data Scraping and Google Sheets Integration"""

import csv
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


""" - Config_driver is a method that configures the webdriver used to interact with the Chrome browser. It sets the options for the Chrome browser, such as whether it should run in headless mode or not.
    - Options is an instance of webdriver.ChromeOptions that is used to set the options for the Chrome browser.
    - If self.headless is True, then the –headless argument is added to the options object. This tells the Chrome browser to run in headless mode.
    - 's' is an instance of Service that starts the ChromeDriver server. The ChromeDriverManager().install() method is used to download and install the latest version of ChromeDriver.
    - driver is an instance of webdriver.Chrome that is created using the service and options objects.
    - self.driver is set to the driver instance so that it can be used to interact with the Chrome browser in other methods."""


# Configuring the selenium webdriver
class GoogleMapScraper:
    def __init__(self):
        self.output_file_name = "google_map_business_data.csv"
        self.headless = False
        self.driver = None
        self.unique_check = []

    def config_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
        self.driver = driver

    # Saving the data
    def save_data(self, data):
        header = [
            "id",
            "company_name",
            "rating",
            "reviews_count",
            "address",
            "category",
            "phone",
            "website",
        ]
        with open(
            self.output_file_name, "a", newline="", encoding="utf-8-sig"
        ) as csvfile:
            writer = csv.writer(csvfile)
            if data[0] == 1:
                writer.writerow(header)
            writer.writerow(data)

    # Contact info:
    def parse_contact(self, business):
        try:
            contact = (
                business.find_elements(By.CLASS_NAME, "W4Efsd")[3]
                .text.split("·")[-1]
                .strip()
            )
        except:
            contact = ""

        if "+1" not in contact:
            try:
                contact = (
                    business.find_elements(By.CLASS_NAME, "W4Efsd")[4]
                    .text.split("·")[-1]
                    .strip()
                )
            except:
                contact = ""

        return contact

    # Rating & Reviews Count:
    def parse_rating_and_review_count(self, business):
        try:
            reviews_block = business.find_element(By.CLASS_NAME, "AJB7ye").text.split(
                "("
            )
            rating = reviews_block[0].strip()
            reviews_count = reviews_block[1].split(")")[0].strip()
        except:
            rating = ""
            reviews_count = ""

        return rating, reviews_count

    # Address & Category:
    def parse_address_and_category(self, business):
        try:
            address_block = business.find_elements(By.CLASS_NAME, "W4Efsd")[
                2
            ].text.split("·")
            if len(address_block) >= 2:
                address = address_block[1].strip()
                category = address_block[0].strip()
            elif len(address_block) == 1:
                address = ""
                category = address_block[0]
        except:
            address = ""
            category = ""

        return address, category

    # Parsing the Data
    def get_business_info(self):
        time.sleep(2)
        for business in self.driver.find_elements(By.CLASS_NAME, "THOPZb"):
            name = business.find_element(By.CLASS_NAME, "fontHeadlineSmall").text
            rating, reviews_count = self.parse_rating_and_review_count(business)
            address, category = self.parse_address_and_category(business)
            contact = self.parse_contact(business)
            try:
                website = business.find_element(By.CLASS_NAME, "lcr4fd").get_attribute(
                    "href"
                )
            except NoSuchElementException:
                website = ""

            unique_id = "".join(
                [name, rating, reviews_count, address, category, contact, website]
            )
            if unique_id not in self.unique_check:
                data = [
                    name,
                    rating,
                    reviews_count,
                    address,
                    category,
                    contact,
                    website,
                ]
                self.save_data(data)
                self.unique_check.append(unique_id)

    """
    The load_companies method is used to load more data. 
    First, the function opens the URL and selects the panel using a pre-defined xpath which we will be using to scroll down the page. 
    The function continues to load data and call get_business_info for each subsequent page until it reaches the end of the page, which is indicated by the appearance of a specific text. 
    At this point, the function sets a flag to stop the while loop and terminates the scraping process.

    """

    # Scrolling down the page to load more data
    def load_companies(self, url):
        print("Getting business info", url)
        self.driver.get(url)
        time.sleep(5)
        panel_xpath = (
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
        )
        panel_xpath = (
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
        )
        scrollable_div = self.driver.find_element(By.XPATH, panel_xpath)
        # scrolling
        flag = True
        i = 0
        while flag:
            print(f"Scrolling to page {i + 2}")
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div
            )
            time.sleep(2)

            if "You've reached the end of the list." in self.driver.page_source:
                flag = False

            self.get_business_info()
            i += 1


urls = [
    "https://www.google.com/maps/search/Restaurants+Canada,+near,+Queen+Street+West,+Toronto,+ON,+Canada/@43.6427771,-79.4437053,15z/data=!3m1!4b1?entry=ttu"
]

business_scraper = GoogleMapScraper()
business_scraper.config_driver()
for url in urls:
    business_scraper.load_companies(url)

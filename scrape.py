from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://svcebookmyevent.in/")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "upcoming"))
)

soup = BeautifulSoup(driver.page_source, "lxml")
driver.quit()

event = soup.find("div", class_="each-event-card-event aos-init")
event_name = event.find("div", class_="each-event-event-info").h3.text
event_venue = event.find("div", class_="each-event-event-info").h5.text
event_inner = event.find("div", class_="each-event-event-info")
event_date = event_inner.find_all("h5", class_="each-event-view-event-details")[1].text
print(event_name)
print(event_venue)
print(event_date)

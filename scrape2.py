from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://svcebookmyevent.in/")

elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "root"))
)

for index, element in enumerate(elements):
    element.click()

    # Wait for the updated element and get nested content
    updated_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "view-more"))
    )
    card = updated_element.find_element(By.CLASS_NAME, "view-card").text
    print(f"Card content for element {index + 1}: {card}")

driver.quit()

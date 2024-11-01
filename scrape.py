import os

from bs4 import BeautifulSoup
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


# Define the function you want to run (e.g., a sample Python script)
def run_python_script(user_input):
    # Check if the user input matches the trigger phrase
    if user_input.lower() == "run script":
        # Set up headless Chrome options
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            # Open the website and wait for the content to load
            driver.get("https://svcebookmyevent.in/")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "upcoming"))
            )

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "lxml")
            events = soup.find_all("div", class_="each-event-card-event aos-init")

            # Gather event information
            event_details = []
            for element in events:
                event_name = element.find("div", class_="each-event-event-info").h3
                event_venue = element.find("div", class_="each-event-event-info").h5
                event_inner = element.find("div", class_="each-event-event-info")
            event_date = event_inner.find_all(
                "h5", class_="each-event-view-event-details"
            )[1].text

            # Check if elements are found before extracting text
            if event_name and event_venue and len(event_date) > 1:
                event_details.append(
                    f"Event: {event_name.text}, Venue: {event_venue.text}, Date: {event_date[1].text}"
                )

            # Prepare the result message
            result = (
                "\n".join(event_details)
                if event_details
                else "No upcoming events found."
            )

        except Exception as e:
            result = f"An error occurred: {str(e)}"

        finally:
            driver.quit()
    else:
        result = "Send 'run script' to see the output of the script."

    return result


@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    # Get the incoming message text
    incoming_msg = request.form.get("Body").strip()

    # Process the message and get a response
    script_output = run_python_script(incoming_msg)

    # Prepare Twilio response
    resp = MessagingResponse()
    resp.message(script_output)
    return str(resp)


if __name__ == "__main__":
    # Use ngrok for local testing or deploy to a server
    app.run(debug=True)

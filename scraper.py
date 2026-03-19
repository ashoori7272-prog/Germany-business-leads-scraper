from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Setup driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open search page
url = "https://www.gelbeseiten.de/Suche/restaurant/Düsseldorf"
driver.get(url)

time.sleep(5)

# Accept cookies on main page
try:
    accept_button = driver.find_element(By.XPATH, "//button[contains(., 'Alle akzeptieren')]")
    accept_button.click()
    time.sleep(2)
except:
    pass

# Get all businesses
businesses = driver.find_elements(By.CSS_SELECTOR, "article")

print("Total businesses found:", len(businesses))
print("=" * 50)

data = []

# Loop through businesses
for b in businesses:
    try:
        name = b.find_element(By.TAG_NAME, "h2").text
        link = b.find_element(By.TAG_NAME, "a").get_attribute("href")

        # Open new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])

        driver.get(link)
        time.sleep(3)

        # Accept cookies on detail page
        try:
            accept_button = driver.find_element(By.XPATH, "//button[contains(., 'Alle akzeptieren')]")
            accept_button.click()
            time.sleep(2)
        except:
            pass

        # Click phone button if exists
        try:
            button = driver.find_element(By.XPATH, "//button[contains(., 'Telefon')]")
            button.click()
            time.sleep(2)
        except:
            pass

        # Extract phone
        try:
            phone_element = driver.find_element(By.XPATH, "//a[contains(@href, 'tel:')]")
            phone = phone_element.text
        except:
            phone = "No phone"

        print("Name:", name)
        print("Link:", link)
        print("Phone:", phone)
        print("-" * 50)

        # Save data
        data.append({
            "name": name,
            "link": link,
            "phone": phone
        })

        # Close tab and return
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except:
        pass

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("leads.csv", index=False)

print("Data saved to leads.csv")

# Close browser
driver.quit()
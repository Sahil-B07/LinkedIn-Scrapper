from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time, getpass

def logedIn():

    expected_url = "https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"
    
    username = input("Username: ")
    password = getpass.getpass()

    driver.get('https://linkedin.com')
    print("logging in....")

    time.sleep(1)
    driver.find_element(
        By.XPATH, "//input[@name = 'session_key']").send_keys(username)
    driver.find_element(
        By.XPATH, "//input[@name = 'session_password']").send_keys(password)

    loginBtn = driver.find_element(By.XPATH, "//button[@type = 'submit']")
    driver.execute_script("arguments[0].click()", loginBtn)
    time.sleep(1)

    if driver.current_url == expected_url:
        print("Successfully logged in.")
    else:
        print("Login Failed!!!\nTry again.\n")
        time.sleep(2)
        logedIn()


def sendInv(maxInv):

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class = 'artdeco-pagination__pages artdeco-pagination__pages--number']/child :: li/child::button")))
    
    pageBtns = [pg.text for pg in driver.find_elements(
        By.XPATH, "//ul[@class = 'artdeco-pagination__pages artdeco-pagination__pages--number']/child :: li/child::button")]
    noPages = int(pageBtns[-1])
    counter = 0

    for i in range(1, noPages):
        
        if counter == maxInv:
            print("Task Completed.")
            break
        
        time.sleep(2)

        if i > 1:
            driver.get(base_url.replace('INDEX', str(i)))
            time.sleep(2)
            
        allButtons = driver.find_elements(By.TAG_NAME, "button")
        inviteBtns = [btn for btn in allButtons if (btn.text == 'Connect' or btn.text == 'Message')]

        for button in inviteBtns:
            
            if button.text == "Connect":
                profile = button.get_attribute(
                    "aria-label").split(" ")

                fname = profile[1]
                lname = profile[2]

                driver.execute_script("arguments[0].click();", button)

                time.sleep(2)

                addNote = driver.find_elements(By.TAG_NAME, "button")
                noteBtn = [btn for btn in addNote if btn.text == 'Add a note']

                if len(noteBtn) > 0:
                    driver.execute_script("arguments[0].click();", noteBtn[0])

                    invMsg = driver.find_element(
                        By.XPATH, "//textarea[@id = 'custom-message']").send_keys("Hi, I'm Sahil.")
                    time.sleep(1)
                    closeInv = driver.find_element(
                        By.XPATH, "//button[@aria-label = 'Dismiss']")
                    driver.execute_script("arguments[0].click();", closeInv)
                    counter += 1
                    print(f"Invitation sent to {fname} {lname}.(C)")
                    if counter == maxInv:
                        break
                else:
                    closeInv = driver.find_element(
                        By.XPATH, "//button[@aria-label = 'Dismiss']").click()
            
            elif button.text == 'Message':
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)

                Btns = driver.find_elements(By.TAG_NAME, "button")
                sendBtn = [btn.text for btn in Btns if btn.text == 'Send']

                if len(sendBtn) > 0:
                    profile = driver.find_element(By.XPATH, "//a[@class='msg-compose__profile-link ember-view']").text.split(" ")
                    fname = profile[0]
                    lname = profile[1]
                    
                    invMsg = driver.find_element(
                            By.XPATH, "//div[@aria-label = 'Write a message…']/child::p").send_keys("Hi, I'm Sahil.")
                    time.sleep(1)
                    
                    closeInv = driver.find_element(
                        By.XPATH, "//li-icon[@type = 'cancel-icon']/parent::button[@class = 'msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']")
                    driver.execute_script("arguments[0].click();", closeInv)
                    counter += 1
                    print(f"Invitation sent to {fname} {lname}.(M)")
                    if counter == maxInv:
                        break
                else:
                    closeInv = driver.find_element(
                        By.XPATH, "//button[@aria-label = 'Dismiss']").click()

    print(f"Total {counter} invites have been sent.")
    driver.quit()

if __name__ == '__main__':

    # chrome_options = Options()
    # chrome_options.add_argument("--headless") , options=chrome_options

    PATH = Service('./chromedriver') 
    driver = webdriver.Chrome(service=PATH)
    
    logedIn()

    # loading filtered page
    base_url = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&keywords=Masters%20Computer%20Science%20Student&origin=GLOBAL_SEARCH_HEADER&page=INDEX'
    driver.get(base_url.replace('INDEX', '1'))
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    
    maxInv = 8

    sendInv(maxInv)


''' 
webdev232002@gmail.com

 '''
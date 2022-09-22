from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time, getpass, logging

def logedIn():

    expected_url = "https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"
    
    username = input("Username: ")
    password = getpass.getpass()

    driver.get('https://linkedin.com')
    logging.info("logging in....")

    time.sleep(1)
    driver.find_element(
        By.XPATH, "//input[@name = 'session_key']").send_keys(username)
    driver.find_element(
        By.XPATH, "//input[@name = 'session_password']").send_keys(password)

    loginBtn = driver.find_element(By.XPATH, "//button[@type = 'submit']")
    driver.execute_script("arguments[0].click()", loginBtn)
    time.sleep(1)

    if driver.current_url == expected_url:
        logging.info("Successfully logged in.")
    else:
        logging.info("Login Failed!!! Try again.")
        time.sleep(2)
        logedIn()


def sendInv(maxInv):
    counter = 0

    for i in range(1, 100):
        
        if counter == maxInv:
            logging.info("Task Completed.")
            break
    
        if i > 1:
            driver.get(base_url.replace('INDEX', str(i)))
            
        time.sleep(3)

        allButtons = driver.find_elements(By.TAG_NAME, "button")
        inviteBtns = [btn for btn in allButtons if (btn.text == 'Connect' or btn.text == 'Message')]

        for button in inviteBtns:
            try:
            
                if button.text == "Connect":
                    profile = button.get_attribute(
                        "aria-label").split(" ")

                    fname = profile[1]
                    lname = profile[2]
                    profile_link = driver.find_element(By.XPATH, "//span[@class='entity-result__title-text t-16']/child::a").get_attribute("href")

                    driver.execute_script("arguments[0].click();", button)

                    time.sleep(2)

                    addNote = driver.find_elements(By.TAG_NAME, "button")
                    noteBtn = [btn for btn in addNote if btn.text == 'Add a note']

                    if len(noteBtn) > 0:
                        driver.execute_script("arguments[0].click();", noteBtn[0])

                        invMsg = driver.find_element(
                            By.XPATH, "//textarea[@id = 'custom-message']").send_keys("Hi, I'm a DevEloper\n\nTesting my bot Please pardon me.")
                        time.sleep(1)

                        closeInv = driver.find_element(
                            By.XPATH, "//button[@aria-label = 'Dismiss']")
                        driver.execute_script("arguments[0].click();", closeInv)
                        counter += 1
                        logging.info(f"Invitation sent to {fname} {lname}.(C) Link: {profile_link}")
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
                        profile_link = driver.find_element(By.XPATH, "//a[@class = 'msg-compose__profile-link ember-view']").get_attribute("href")

                        
                        invMsg = driver.find_element(
                                By.XPATH, "//div[@aria-label = 'Write a message…']/child::p").send_keys("Hi, I'm DevEloper\n\nJust testing my bot Please pardon me.")
                        time.sleep(1)
                        
                        closeInv = driver.find_element(
                            By.XPATH, "//li-icon[@type = 'cancel-icon']/parent::button[@class = 'msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']")
                        driver.execute_script("arguments[0].click();", closeInv)
                        time.sleep(3)

                        try:
                            discardBtn = driver.find_element(By.XPATH, "//button[@class = 'artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
                            driver.execute_script("arguments[0].click();", discardBtn)
                        except Exception as e:
                            logging.error(e)

                        counter += 1
                        logging.info(f"Invitation sent to {fname} {lname}.(M) Link: {profile_link}")
                        if counter == maxInv:
                            break
                    else:
                        closeInv = driver.find_element(
                            By.XPATH, "//button[@aria-label = 'Dismiss']").click()
            
            except Exception as e:
                logging.error(e)

    logging.info(f"Total {counter} invites have been sent.\n")
    driver.quit()

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO,filename="LogFile.log",
                    format='%(asctime)s %(levelname)s:%(message)s')

    PATH = Service('./chromedriver') 
    driver = webdriver.Chrome(service=PATH)
    
    logedIn()

    # loading filtered page
    base_url = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&keywords=Masters%20Computer%20Science%20Student&origin=GLOBAL_SEARCH_HEADER&page=INDEX'
    driver.get(base_url.replace('INDEX', '1'))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    
    maxInv = 10

    sendInv(maxInv)
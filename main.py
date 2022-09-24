from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, getpass, logging, os, csv

def logedIn():

    expected_url = "https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"
    
    username = input("Username/Email: ")
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
    rows = []
    fields = [["Name", "Link", "Flag"]]

    for i in range(1, 100):
        
        if counter == maxInv:
            break
    
        if i > 1:
            driver.get(base_url.replace('INDEX', str(i)))
            
        time.sleep(2)
        allButtons = driver.find_elements(By.TAG_NAME, "button")
        inviteBtns = [btn for btn in allButtons if (btn.text == 'Connect' or btn.text == 'Message')]

        for button in inviteBtns:
            try:
            
                if button.text == "Connect":
                    profile = button.get_attribute("aria-label").split(" ")
                    inName = profile[1] +" "+profile[2]
                    profile_link = driver.find_element(By.XPATH, "//span[@dir = 'ltr']/parent::a[@class = 'app-aware-link']").get_attribute("href")
                    flag = "C"

                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)

                    addNote = driver.find_elements(By.TAG_NAME, "button")
                    noteBtn = [btn for btn in addNote if btn.text == 'Add a note']

                    sendBtn = [btn for btn in addNote if btn.text == 'Send']
                    # To send message use....., line 78 after invMsg......and line 82 comment closeInv ->,  driver.execute_script("arguments[0].click();", sendBtn) 

                    if len(noteBtn) > 0:
                        driver.execute_script("arguments[0].click();", noteBtn[0])

                        invMsg = driver.find_element(
                            By.XPATH, "//textarea[@id = 'custom-message']").send_keys("Hi, I'm a DevEloper\n\nTesting my bot Please pardon me.")
                        time.sleep(1)

                        closeInv = driver.find_element(
                            By.XPATH, "//button[@aria-label = 'Dismiss']")
                        driver.execute_script("arguments[0].click();", closeInv)
                        counter += 1
                        logging.info(f"Invitation sent to {inName}.(C) Link: {profile_link}")
                        rows.append([inName, profile_link, flag])
                        if counter == maxInv:
                            break
                    else:
                        closeInv = driver.find_element(
                            By.XPATH, "//button[@aria-label = 'Dismiss']").click()
                
                elif button.text == "Message":
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)
                    
                    Btns = driver.find_elements(By.TAG_NAME, "button")
                    # To send message use....., line 110 after invMsg......and line 114 comment closeInv ->,  driver.execute_script("arguments[0].click();", sendBtn) 
                    sendBtn = [btn.text for btn in Btns if btn.get_attribute('class') == 'msg-form__send-button artdeco-button artdeco-button--1']

                    if len(sendBtn) > 0:
                        pid = driver.find_element(By.XPATH, "//a[@class='msg-compose__profile-link ember-view']")
                        profile = pid.text.split(" ")
                        inName = profile[0] +" "+profile[1]
                        profile_link = pid.get_attribute("href")
                        flag = "M"
                        
                        invMsg = driver.find_element(
                                By.XPATH, "//div[@aria-label = 'Write a message…']/child::p").send_keys("Hi, I'm DevEloper\n\nJust testing my bot Please pardon me.")
                        time.sleep(1)
                        
                        closeInv = driver.find_element(
                            By.XPATH, "//li-icon[@type = 'cancel-icon']/parent::button[@class = 'msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']")
                        driver.execute_script("arguments[0].click();", closeInv)
                        time.sleep(2)

                        try:
                            discardBtn = driver.find_element(By.XPATH, "//button[@class = 'artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
                            driver.execute_script("arguments[0].click();", discardBtn)
                        except Exception as e:
                            logging.error(e)

                        counter += 1
                        logging.info(f"Invitation sent to {inName}.(M) Link: {profile_link}")
                        rows.append([inName, profile_link, flag])
                        if counter == maxInv:
                            break
                    else:
                        closeInv = driver.find_element(
                            By.XPATH, "//button[@aria-label = 'Dismiss']")
                        driver.execute_script("arguments[0].click();", closeInv)

            except Exception as e:
                logging.error(e)
    
    # saving the user data to whom invitation is addressed
    

    if not os.path.isfile(os.path.join(os.getcwd(), "data.csv")):
        with open('data.csv', 'a', newline='') as f:
            write = csv.writer(f) 
            write.writerows(fields) 
            write.writerows(rows) 
    else:
        with open('data.csv', 'a', newline='') as f:
            write = csv.writer(f) 
            write.writerows(rows) 
        
    logging.info(f"Total {counter} invites have been sent.")
    driver.quit()

if __name__ == '__main__':

    # basic log file settings
    logging.basicConfig(level=logging.INFO,filename="logFile.log",format='%(asctime)s %(levelname)s:%(message)s')

    PATH = Service('./chromedriver') 

    # enable chrome options 
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")

    # setting the driver
    driver = webdriver.Chrome(service=PATH, options=chrome_options)

    maxInv = int(input("Max Results: "))
    logedIn()  # Logging function

    # loading filtered page
    base_url = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&keywords=Masters%20Computer%20Science%20Student&origin=GLOBAL_SEARCH_HEADER&page=INDEX'
    driver.get(base_url.replace('INDEX', '1'))
    time.sleep(2)

    sendInv(maxInv)  # Send invitaions function
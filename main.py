from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import time

# Function to initialize the webdriver and open the webpage
def initialize_webdriver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def click_start_button(driver):
    button = driver.find_element(By.CLASS_NAME, 'button--big')
    button.click()


def save_results(results):
    csv_file = "results.csv"
    with open(csv_file, 'w') as f:
        w = csv.DictWriter(f, results.keys())
        w.writeheader()
        w.writerow(results)


# Function to navigate through questions, answer them, and capture text
def navigate_and_answer(driver):
    questions = driver.find_elements(By.CLASS_NAME, 'theses__text')
    print('len questions: ', len(questions))
    buttons = driver.find_elements(By.CLASS_NAME, 'theses-btn')
    results = {}

    while True:
        slider = driver.find_elements(By.ID, 'theses-slider')

        try:
            index = int(slider[0].text[6:8].split('/')[0])
            index = index-1
            
            try:
                question = questions[index]     
                button1, button2, button3 = buttons[index*3: index*3+3]
                print('Question: ', question.text)
                print('Option 1: ', button1.text.split('\n')[0])
                print('Option 2: ', button2.text.split('\n')[0])
                print('Option 3: ', button3.text.split('\n')[0])
                idx = int(input('Enter you answer 1, 2 ,3: '))
                if(idx == 1):
                    button1.click()
                elif(idx == 2):
                    button2.click()
                elif(idx == 3):
                    button3.click()
                
                results[question.text] = button1.text.split('\n')[0] if idx == 1 else button2.text.split('\n')[0] if idx == 2 else button3.text.split('\n')[0]
                

            except:
                continue
        except:
            if(index == len(questions)-1):
                print("exiting")
                return results    
            continue

        
        time.sleep(1.5)
        


            
        
        


if __name__ == "__main__":
    url = 'https://www.wahl-o-mat.de/bundestagswahl2021/app/main_app.html'
    driver = initialize_webdriver(url)
    click_start_button(driver)
    
    answers = navigate_and_answer(driver)
    save_results(answers)
    driver.close()
    driver.quit()

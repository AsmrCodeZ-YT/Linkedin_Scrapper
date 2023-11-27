import yaml
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#open config file 
with open('../config.yml', 'r') as file:
    prime_service = yaml.safe_load(file)

time  = prime_service["TIME"]
username = prime_service["USERNAME"]
password = prime_service["PASSWORD"]


service = Service("../00_WebDriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(prime_service["URL"])
driver.find_element(By.XPATH ,'/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input').send_keys(username)
driver.find_element(By.XPATH ,'/html/body/main/section[1]/div/div/form/div[1]/div[2]/div/div/input').send_keys(password)
driver.find_element(By.XPATH ,'//*[@id="main-content"]/section[1]/div/div/form/div[2]/button').click()

# bot skip
bot_skip = prime_service["BotSkip"]
if  bot_skip:
    sleep(prime_service["TIME_Bot_HANDLE"])


sleep(time)

page = prime_service["PAGE"]
new_link = prime_service["URL3"]

with open(prime_service["EXPORT_FILE2"] , "w" ,encoding="UTF-8") as f1: 
    writer = csv.writer(f1, delimiter=',',lineterminator='\n',)
    
    
    for page_start in range(0 , page*5, 25):
        
        # create new link for pages
        page_start = str(page_start)
        if "start" in new_link:
            idx = new_link.index("start")
            new_link = new_link[:idx + 6] + page_start
        
        print(new_link)
        driver.get(new_link)
        
        sleep(5)
        for i in range(1,25):
                    
            About_the_job = ""
            
            temp_link = f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[1]/div/ul/li[{i}]/div/div[1]/div[1]/div[2]/div[1]/a"
            try:
                driver.find_element(By.XPATH ,temp_link).click()
                link = driver.find_element(By.XPATH ,temp_link).get_attribute("href")
                sleep(5)
            except:
                link = None 
            
            
            
            # title_job 
            titlejob_xpath = "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/a/h2"
            try:
                titlejob = driver.find_element(By.XPATH ,titlejob_xpath).text
            except:
                titlejob = None
                
            #others 
            others_xpath = "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]"
            try:
                others = driver.find_element(By.XPATH ,others_xpath).text
                if "," in others :
                    others = others.replace(",", " ")
            except:
                others = None
                
            # extract  About_the_job
            for i in range(2,6):
                About_the_job_xpath = f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div/div[1]/div/div[{i}]"
                try:
                    text = driver.find_element(By.XPATH ,About_the_job_xpath).text
                    text = text.replace(",", " ")
                    
                    if "About the job" in text:
                        About_the_job += text
                        break
                except:
                    About_the_job = None
                    
            
            row = [titlejob,others,About_the_job,link]
            print(row)
            writer.writerow(row)
            
            # stop for scrolling
            if i%5==0:
                sleep(2)

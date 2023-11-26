import yaml
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#open config file 
with open('../config.yml', 'r') as file:
    prime_service = yaml.safe_load(file)


COUNT = prime_service["COUNT"]
time  = prime_service["TIME"]
username = prime_service["USERNAME"]
password = prime_service["PASSWORD"]

# service = Service(prime_service["PATH"])
service = Service("../00_WebDriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(prime_service["URL"])
driver.find_element(By.XPATH ,'/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input').send_keys(username)
driver.find_element(By.XPATH ,'/html/body/main/section[1]/div/div/form/div[1]/div[2]/div/div/input').send_keys(password)
driver.find_element(By.XPATH ,'//*[@id="main-content"]/section[1]/div/div/form/div[2]/button').click()


bot_skip = prime_service["BotSkip"]
if  bot_skip:
    sleep(prime_service["TIME_Bot_HANDLE"])
    

# got to network
driver.get(prime_service["URL2"])
sleep(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(10)

##################################################################
bool_ = False
num = 1
for i in range(1,10):
    try:
        h2_title_xpath = f"/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/section[2]/div/div[1]/div[{i}]/div[1]/h2"
        h2_title       = driver.find_element(By.XPATH ,h2_title_xpath).text
        print(h2_title)
        if "Popular people to follow" in h2_title:
            num = i
            bool_ = True
            break
    except:
        pass
        
assert bool_ == True 


num2 = 5
for i in range(1,10):
    try:
        seeall_btn = f"/html/body/div[{i}]/div[3]/div/div/div/div/div[2]/div/div/main/section[2]/div/div[1]/div[{num}]/div[1]/button"
        driver.find_element(By.XPATH ,seeall_btn).click()
        sleep(10)
        num2 = i
        print("Done")   
        break
    except:
        pass


with open(prime_service["EXPORT_FILE"], "w" ,encoding="utf-8") as f1 :
    writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
    for i in range(1,COUNT):
        div1 = f"/html/body/div[3]/div/div/div[2]/section/div/div[1]/ul/li[{i}]/div/li/div/section/div[2]/div[1]"
        div2 = f"/html/body/div[3]/div/div/div[2]/section/div/div[1]/ul/li[{i}]/div/li/div/section/div[2]/div[2]"
        
        try:
            link_div1 = div1 + "/a"
            link      = driver.find_element(By.XPATH ,link_div1).get_attribute("href")
        except:
            link = None
        
        try:
            name_div1    = div1 + "/a/span[2]"
            name     = driver.find_element(By.XPATH ,name_div1).text
        except:
            name = None
        
        try:
            title_div1   = div1 + "/a/span[4]"
            title     = driver.find_element(By.XPATH ,title_div1).text
        except:
            title = None
        
        
        ####  more options find count of followers and talk about : need work on it : have bug
        # try:    
        #     text_p    = div2 + "/p"
        #     text_finder      = driver.find_element(By.XPATH ,text_p).text
        #     follower = None
        #     talk = None
        #     if ("followers" in text_finder) and ("talk about" in text_finder):
        #         text_p1   = div2 + "/p[1]"
        #         text_p2    = div2 + "/p[2]"
        #         follower = driver.find_element(By.XPATH ,text_p1).text
        #         talk = driver.find_element(By.XPATH ,text_p2).text
        #         follower = follower
        #         talk = talk
                
        #     elif ("followers" in text_finder):
        #         follower = driver.find_element(By.XPATH ,text_p).text
        #         follower = follower
                
        #     else:
        #         talk = driver.find_element(By.XPATH ,text_p).text
        #         talk = talk

        # except:
        #     follower ,talk = None,None
        
        # row = [i,name,title,follower,talk]
        
        
        row = [i,name,title,link]
        writer.writerow(row)
        # stop for scrolling
        if i%5==0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
        


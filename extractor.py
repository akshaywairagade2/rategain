from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

columns = ['BlogImageURL', 'BlogTitle', 'BlogDate', 'BlogLikesCount']
df = pd.DataFrame(columns=columns)


def getImageData(child_element):
    image_element=child_element.find_element(by=By.CLASS_NAME, value="img")
    anchor_element = image_element.find_element(By.TAG_NAME, "a")
    url = anchor_element.get_attribute("data-bg")
    return url

def getHeading(content):
    heading_element=content.find_element(By.TAG_NAME, "h6")
    anchor_element = heading_element.find_element(By.TAG_NAME, "a")
    return anchor_element.text

def getDate(content):
    blog_detail_element=content.find_element(By.CLASS_NAME, "blog-detail")
    date_element=blog_detail_element.find_element(By.CLASS_NAME, "bd-item")
    return date_element.text

def getLikes(content):
    likes_element=content.find_element(By.CLASS_NAME,"zilla-likes")
    return likes_element.text

def getContent(child_element):
    content=child_element.find_element(by=By.CLASS_NAME, value="content")
    heading=getHeading(content)
    date=getDate(content)
    likes=getLikes(content)
    return (heading,date,likes)



PATH="C:\SeleniumDrivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get("https://rategain.com/blog")


while(True):
    sleep(3)
    xPath="//article[@class='blog-item category-blog with-image ']"
    blogs=driver.find_elements(by=By.XPATH,value=xPath)
    for i in range(len(blogs)):
        child_element=blogs[i].find_element(by=By.CLASS_NAME, value='wrap')
        url=getImageData(child_element)
        heading,date,likes=getContent(child_element)
        row = {'BlogImageURL': url, 'BlogTitle': heading, 'BlogDate': date, 'BlogLikesCount': likes}
        df = df.append(row, ignore_index=True)
    try:
        next_page=driver.find_element(by=By.XPATH, value="//a[@class='next page-numbers']")
        next_page_link=next_page.get_attribute("href")
        driver.get(next_page_link)
        sleep(2)
    except:
        break
    print(len(df))

csv_file_path = 'final_data.csv'
df.to_csv(csv_file_path, index=False)
# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

# setting up selenium and opening the website
PATH="C:\SeleniumDrivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get("https://rategain.com/blog")

# initializing our dataframe for storing the results
columns = ['BlogImageURL', 'BlogTitle', 'BlogDate', 'BlogLikesCount']
df = pd.DataFrame(columns=columns)

# gets the url of the image
def getImageData(child_element):
    image_element=child_element.find_element(by=By.CLASS_NAME, value="img")
    anchor_element = image_element.find_element(By.TAG_NAME, value="a")
    url = anchor_element.get_attribute("data-bg")
    return url

# gets the heading of the content
def getHeading(content):
    heading_element=content.find_element(By.TAG_NAME, value="h6")
    anchor_element = heading_element.find_element(By.TAG_NAME,value= "a")
    return anchor_element.text

# gets the date of the blog publishment
def getDate(content):
    blog_detail_element=content.find_element(By.CLASS_NAME,value= "blog-detail")
    date_element=blog_detail_element.find_element(By.CLASS_NAME,value= "bd-item")
    return date_element.text

# get count of likes for the blog
def getLikes(content):
    likes_element=content.find_element(By.CLASS_NAME,value="zilla-likes")
    return likes_element.text

# calls other functions to get the blog data
def getContent(child_element):
    content=child_element.find_element(by=By.CLASS_NAME, value="content")
    heading=getHeading(content)
    date=getDate(content)
    likes=getLikes(content)
    return (heading,date,likes)


# we run the program until there is no next page left 
# we add the sleep for smooth loading of the next page
# fetching of the data is done accordingly to classes 
# various functions are implemented to keep the code clean
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


# after final calculations data is stored in CSV format 
csv_file_path = 'final_data_.csv'
df.to_csv(csv_file_path, index=False)
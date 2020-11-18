from seleniumwire import webdriver
import selenium.common.exceptions
import theScrapper
import random
import time
import sys
page=str(sys.argv[1])
#region=str(sys.argv[1])
region='Orlando'
driver=webdriver.Firefox()
driver.get("https://www.indeed.com/jobs?q=software&l=Orlando,+FL&start=%s"%page)
def sleepRandom(x,y):
  n=random.randint(x,y)
  time.sleep(random.random()+time.time()/10.01**100.01+n)
def getNextPage(next):
  for i in next:
    exv=i.get_attribute("rel")
    if exv=='next':
      return i.get_attribute("href")
def getHTTP():
    for request in driver.requests:
      if request.response:
        if str(request.path).find('viewtype=embedded&jk')>0:
          event=theScrapper.collector(region,str(request.path))
          event.getJobData()
def iterpage():
  titles=driver.find_elements_by_class_name("title")
  for title in titles:
    title.click()
    getHTTP()
    sleepRandom(6,10)
while True:
  nextPage=None
  try:
    iterpage()
    sleepRandom(3,5)
    next=driver.find_elements_by_css_selector("link")
    nextPage=getNextPage(next)
    driver.get(nextPage)
  except selenium.common.exceptions.StaleElementReferenceException:
        driver.refresh()
        sleepRandom(2,3)
  except selenium.common.exceptions.ElementClickInterceptedException:
        driver.refresh()
        sleepRandom(2,3)
  except selenium.common.exceptions.InvalidArgumentException:
        driver.refresh()
        sleepRandom(2,3)

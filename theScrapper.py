from tinydb import TinyDB,Query
from bs4 import BeautifulSoup
import dictionary
import requests

class collector:

  def __init__(self,region,embedded_url):

    response=requests.get(embedded_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    self.keywords=dictionary.keywords()
    db = TinyDB('employerData.json')
    self.__region=db.table(region)
    self.__embedded_url=embedded_url
    self.__soup=soup

  def getJobData(self):
    def getKeywords(keywords):
      matches=[]
      for keyword in keywords:
        if all_text.find(keyword)>0:
          matches.append(keyword)
      return matches
    job_position=BeautifulSoup(str(self.__soup.title),'html.parser').text
    job_salary=BeautifulSoup(str(self.__soup.findAll("span",class_="icl-u-xs-mr--xs")),'html.parser').text
    job_type=BeautifulSoup(str(BeautifulSoup(str(self.__soup.findAll("div",class_="jobsearch-JobDescriptionSection-sectionItem")),'html.parser').findAll("div",class_=None)),'html.parser').text
    all_text=self.__soup.get_text().lower()
    systems=getKeywords(self.keywords.systems)
    languages=getKeywords(self.keywords.languages)
    softwares=getKeywords(self.keywords.softwares)
    buzzwords=getKeywords(self.keywords.buzzwords)
    academics=getKeywords(self.keywords.academics)
    item=Query()
    item_status=len(self.__region.search(item.embedded_url==self.__embedded_url))
    if item_status>0:
      print("this item already exist, lets upsert it  ^^^^^")
      self.__region.upsert({'job_position': job_position,
                            'job_salary':job_salary,
                            'job_type':job_type,
                            'all_text':all_text,
                            'embedded_url':self.__embedded_url,
                            'systems':systems,
                            'languages':languages,
                            'softwares':softwares,
                            'academics':academics,
                            'buzzwords':buzzwords},item.embedded_url==self.__embedded_url)
    elif item_status<=0:
      print("this is a new item, lets insert it  ---->")
      self.__region.insert({'job_position': job_position,
                            'job_salary':job_salary,
                            'job_type':job_type,
                            'all_text':all_text,
                            'embedded_url':self.__embedded_url,
                            'systems':systems,
                            'languages':languages,
                            'softwares':softwares,
                            'academics':academics,
                            'buzzwords':buzzwords})
    print("title: ", job_position)
    print("salary: ", job_salary)
    print("job type: ", job_type)
    print("matches: ", systems)
    print("languages: ",languages)
    print("softwares: ",softwares)
    print("buzzwords: ",buzzwords)
    print("academics: ",academics)

"""this is a test ""
from tinydb import TinyDB
db = TinyDB('employerData.json')
region=db.table('Tallahasee')
url="https://www.indeed.com/viewjob?viewtype=embedded&jk=2f353b4968d7eeb1&from=vjs&tk=1elpd7p4r34mh000&advn=1530139303758884&adid=358568337&ad=-6NYlbfkN0BItDYe-d4W27lKQWMgoDRqvhI7Kc0F6ykam_em43ldj5VR3ECxXTn12kKd010xgxNDXH-Ak2BUycCTXPq9yZQ9Rj3tXgUFbS01dT9-lwIdYEAvt2gP3Dk8dHLODgciXWwcc-5GrpuRzQl6hz4bk-EcuWrdz5NLeT_jpbhRxKbkZ4PQ7Touo24rb0ivt9veatljfxyKfzz7cvhKydN4-NaVhObXm0C3N8WY7RHx-AADMvqjus3xNy8_u-fmCJDSYE__8tZE8LIPwkjTVJktUihcIEo19llB34FL-lYZ_FcRYIKQpwVXXZZ-0AW5VRdZ-_Zt55r4MYBtF0BF6lTBOvn0ojDEzGt8aP1ShvzfwTHX9Ywq7vHU0wSmrXnK8gFnIWf7TXus87qcZheDSm9qjiYFa-K05RcsVorXpi-gRkUFIu4p0W7PS5FJtEwvjDjQ6mBHOr9MgRtcvcp9tE59sz0AtoIFJZjIg4b6lMWfc9gL2A%3D%3D&topwindowlocation=%2Fjobs%3Fq%3Dsoftware%26l%3DTallahassee%252C%2520FL%26start%3D13%26vjk%3D62bc80f79a39d3df"
test=collector(region,url)
#test=collector(url)
test.getJobData()
"""

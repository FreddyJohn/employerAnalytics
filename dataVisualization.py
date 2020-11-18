from mpld3 import fig_to_html, plugins
import matplotlib.pyplot as plt
from tinydb import TinyDB
import interactive
import numpy as np
import dictionary

db=TinyDB('employerData.json')
region=db.table('Orlando')
#region=db.table('Tallahassee')
words=dictionary.keywords()
languages=words.languages
systems=words.systems
softwares=words.softwares
buzzwords=words.buzzwords
academics=words.academics
all_keywords=languages+systems+softwares+buzzwords+academics
attributes=['languages','systems','softwares','buzzwords','academics']
keywords=[languages,systems,softwares,buzzwords,academics]

def getAllStats(str,keywords):
  arr=[]
  for i in region.all():
    if len(i['job_salary'])>2:
      if i['job_salary'].find(str)>0:
        print("Job Salary: ",i['job_salary']," keywords: ",i[keywords])
        x="".join(c for c in i['job_salary'] if c.isdigit() or c==' ' or c=='.').split()
        for i in range(len(x)):
          x[i]=float(x[i])
        arr.append(np.mean(x))
  return arr

def getStatsForJob(str,item):
  for i in region.all():
    if i['job_position']==item:
      if len(i['job_salary'])>2:
        if i['job_salary'].find(str)>0:
          x="".join(c for c in i['job_salary'] if c.isdigit() or c==' ' or c=='.').split()
          for i in range(len(x)):
            x[i]=float(x[i])
          return np.mean(x)

def plotAllOccurences(keywords,attributes):
  y=np.zeros(len(keywords),dtype=int)
  def recursion(attribute):
    for item in items[attribute]:
      for keyword in keywords:
        if item==keyword:
          y[keywords.index(item)]+=1
          break
  for items in region.all():
    for i in range(len(attributes)):
      recursion(attributes[i])
  print(y)
  print("Total entries: ",len(region.all()))
  for i in range(len(y)):
    percent=y[i]/len(region.all())*100
    word=keywords[i]
    print(word," ", percent,"%")
  fig = plt.figure()
  ax = fig.add_axes([0,0,1,1])
  rects=ax.bar(keywords,y)
  for rect, label in zip(rects, keywords):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label,
            ha='center', va='bottom')
  plt.show()


def plotOccurences(keywords,attribute):
  y=np.zeros(len(keywords),dtype=int)
  for items in region.all():
    for item in items[attribute]:
      for keyword in keywords:
        if item==keyword:
          y[keywords.index(item)]+=1
          break
  print(y)
  print("Total entries: ",len(region.all()))
  for i in range(len(y)):
    percent=y[i]/len(region.all())*100
    word=keywords[i]
    print(word," ", percent,"%")
  fig = plt.figure()
  ax = fig.add_axes([0,0,1,1])
  rects=ax.bar(keywords,y)
  for rect, label in zip(rects, keywords):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label,
            ha='center', va='bottom')
  plt.show()


def clusterJobs(keywords,attribute_1,num):
  x=[]
  y=[]
  words=[]
  z=0
  all_items=region.all()
  fig, ax = plt.subplots()
  all_jobs=[job['job_position'] for job in region.all()]
  for i in range(len(all_items)):
    for j in all_items[i][attribute_1]:
      if all_items[i]['job_salary'].find('year')>0:
        z=getStatsForJob('year',all_items[i]['job_position'])
        print(z)
      words.append(keywords.index(j))
    if len(words)>num:
      feature_1=np.mean(words)
      feature_2=np.std(words)
      x.append(feature_1)
      y.append(feature_2)
      ax.scatter(x=feature_1,y=feature_2,c=['#1f77b4'],alpha=0.5,s=z/1000)
      #ax.annotate(str(all_items[i]['job_salary']),(feature_1,feature_2))
      words.clear()
    elif len(words)<=num:
      all_jobs.remove(all_items[i]['job_position'])

  af =  interactive.AnnoteFinder(x,y, all_jobs, ax=ax)
  fig.canvas.mpl_connect('button_press_event', af)
  plt.xlabel('Mean')
  plt.ylabel('Standard Deviation')
  plt.title('%s Clustering for Local Job Vaccancies'%attribute_1.capitalize())
  plt.show()

def prototype(keywords,attribute_1,attributes,num):
  all_items=region.all()
  words=[]
  def recursion(attribute):
    for j in all_items[i][attribute]:
      words.append(keywords.index(j))
  x=[]
  y=[]
  words=[]
  fig, ax = plt.subplots()
  all_jobs=[job[attribute_1] for job in region.all()]
  for i in range(len(all_items)):
    for j in range(len(attributes)):
      recursion(attributes[j])
    print(words)
    if len(words)>num:
      feature_1=np.mean(words)
      feature_2=np.std(words)
      x.append(feature_1)
      y.append(feature_2)
      print(all_items[i]['job_salary'])
      ax.scatter(x=feature_1,y=feature_2) #,c=colors[j])
      words.clear()
    elif len(words)<=num:
      all_jobs.remove(all_items[i][attribute_1])
  af =  interactive.AnnoteFinder(x,y, all_jobs, ax=ax)
  fig.canvas.mpl_connect('button_press_event', af)
  print(len(x),len(y),len(all_jobs))
  plt.xlabel('Mean')
  plt.ylabel('Standard Deviation')
  plt.title('Keywords Clustering for Local Job Vaccancies')
  plt.show()

#for attribute in attributes:
#  clusterJobs(keywords,'job_position',attribute,2)
for i in range(len(attributes)):
  #plotOccurences(keywords[i],attributes[i])
  clusterJobs(keywords[i],attributes[i],2)
#prototype(all_keywords,'job_position',attributes,0)
#plotAllOccurences(all_keywords,attributes)
#plotOccurences(keywords,'academics')
#year=getAllStats('year','languages')
year=getAllStats('year','languages')
plt.hist(year,bins=60)
plt.show()
#hour=getAllStats('hour','languages')
#plt.hist(hour,bins=60)
#plt.show()
#print("the average salary: ",np.mean(year))
#print("the average hourly pay: ",np.mean(hour))


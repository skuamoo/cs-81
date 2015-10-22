#! python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import string

html = urlopen("http://shakespeare.mit.edu/")
bsObj = BeautifulSoup(html)

hyperlinks = bsObj.findAll("a",href=re.compile("(.html)"))

data = []

for links in hyperlinks:
    if 'href' in links.attrs:
        if(links.attrs['href'] == "news.html"):
            continue
        
        path = str(links.attrs['href'])
        
        end = path.find('/')
        directory = path[0:end]   
        html1 =  urlopen("http://shakespeare.mit.edu/" + links.attrs['href'] )
        bsObj1 = BeautifulSoup(html1)
        
        if(directory != "Poetry"):
            hl2 = bsObj1.findAll("a",href=re.compile("(.html)"))
        else:
            hl2 = bsObj1.findAll("a",href=re.compile("(.html)"))
            #if(not hl2):
                #print("Reading file: http://shakespeare.mit.edu/" + str(links.attrs['href']))
                #content = urlopen("http://shakespeare.mit.edu/" + str(links.attrs['href']))
                #bsObj2 = BeautifulSoup(content)
                #data = data + str(bsObj2.get_text())
                
        for links2 in hl2:
            scene_lines = []
            if(links2.attrs['href'] == "full.html"):
                continue
            if 'href' in links2.attrs and directory != "Poetry":
                link_href = str(links2.attrs['href'])
                #print("Reading file: http://shakespeare.mit.edu/" + directory + "/" + link_href)
                html2 = urlopen("http://shakespeare.mit.edu/" + directory + "/" + link_href)
                bsObj2 = BeautifulSoup(html2)
                hl3 = bsObj2.findAll('a')
                title = bsObj2.find('td').contents[0].strip()
                act_start = link_href.find(".", link_href.find(directory + "."))+1
                act_end = link_href.find(".", act_start)
                act = link_href[act_start:act_end]
                scene = link_href[act_end+1:link_href.find(".html")]                               
                #page = str(bsObj2.contents[1])
                #act = page[page.find("Act")+4:page.find(",", page.find("Act")+4)].strip()
                #scene = page[page.find("Scene")+6:page.find("<", page.find("Scene")+6)].strip()
                for links3 in hl3:
                    if 'name' in links3.attrs:
                        if links3.attrs['name'].isnumeric():
                            scene_lines.append(links3.contents[0].strip())
                text = ' '.join(scene_lines)
                tokens = nltk.word_tokenize(text)
                tokens_cleaned = [word for word in tokens if word.lower() not in stopwords.words('english') and len(word) > 2]
                freq = dict(nltk.FreqDist(tokens_cleaned))
                scene_obj = {'title':title, 'act':act, 'scene':scene, 'lines':scene_lines, 'text':text, 'freq':freq}
            else:
                continue
            data.append(scene_obj)
f = open('shakespeare.txt', 'w')
f.writelines(str(data))
f.close()
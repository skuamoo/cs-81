#! python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import string
from collections import defaultdict
#Open MIT Shakespeare page and extract all links
html = urlopen("http://shakespeare.mit.edu/")
page = BeautifulSoup(html)
play_links = page.findAll("a",href=re.compile("(.html)"))

data_scenes = []
data_acts = []

for link in play_links:
    if 'href' in link.attrs:
        #skip news link
        if(link.attrs['href'] == "news.html"):
            continue
        
        path = str(link.attrs['href'])        
        end = path.find('/')
        directory = path[0:end]   
        html_plays =  urlopen("http://shakespeare.mit.edu/" + link.attrs['href'] )
        plays = BeautifulSoup(html_plays)
        #title = plays.find('td').contents[0].strip()
        if(directory == "Poetry"):
            #Skip poetry due to inherent stylistic differences
            continue
        else:
            act_links = plays.findAll("a",href=re.compile("(.html)"))

        act_text = defaultdict(lambda:defaultdict(list))
        act_lines = defaultdict(lambda:defaultdict(list))
        for link2 in act_links:
            scene_lines = []
            #Skip link to full play
            if(link2.attrs['href'] == "full.html"):
                continue
            if 'href' in link2.attrs:
                link_href = str(link2.attrs['href'])
                #print("Reading file: http://shakespeare.mit.edu/" + directory + "/" + link_href)
                html_acts = urlopen("http://shakespeare.mit.edu/" + directory + "/" + link_href)
                acts = BeautifulSoup(html_acts)
                scenes = acts.findAll('a')
                title = acts.find('td').contents[0].strip()
                act_start = link_href.find(".", link_href.find(directory + "."))+1
                act_end = link_href.find(".", act_start)
                act = link_href[act_start:act_end]
                scene = link_href[act_end+1:link_href.find(".html")]                               
                for link3 in scenes:
                    if 'name' in link3.attrs:
                        if link3.attrs['name'].isnumeric():
                            scene_lines.append(link3.contents[0].strip())
                text = ' '.join(scene_lines)
                tokens = nltk.word_tokenize(text)
                #tokens_cleaned = [word for word in tokens if word.lower() not in stopwords.words('english') and len(word) > 2]
                #freq = dict(nltk.FreqDist(tokens))
                scene_obj = {'title':title, 'act':act, 'scene':scene, 'lines':scene_lines, 'text':text}
                data_scenes.append(scene_obj)
                act_lines[title][act] += scene_lines
                act_text[title][act].append(text)

        for key in sorted(act_lines.keys()):
            for act_num in sorted(act_lines[key].keys()):
                act_obj = {'title':key, 'act':act_num, 'lines':act_lines[key][act_num], 'text':' '.join(act_text[key][act_num])}
                data_acts.append(act_obj)

#Write data by scene to file
f = open('shakespeare_scenes.txt', 'w')
f.writelines(str(data_scenes))
f.close()
#Write data by act to file
f = open('shakespeare_acts.txt', 'w')
f.writelines(str(data_acts))
f.close()
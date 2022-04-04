#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import datetime 

url = 'https://www.rimosco.it/picalendar/index.php?a=list'
r = requests.get(url)
pical_problems = BeautifulSoup(r.text, 'html.parser')
data = [ [l.split(" (Risolto ")[0],int(l.split(" (Risolto ")[1])] 
        for l in pical_problems.text.split("\n")[20].split(" volte)")[:-1] ]
labels = [ l[0] for l in np.array(data)[:,0:1] ]
values = [ int(l[0]) for l in np.array(data)[:,1:] ]

now = str(datetime.datetime.now())[:16]

fig, ax = plt.subplots(figsize=(12,8),dpi=100)
plt.bar(labels,values)
plt.xticks(range(len(labels)), labels, rotation='vertical')
fig.subplots_adjust(bottom=0.35)
ax.set_xlabel('Problema', labelpad=15)
ax.set_ylabel('Soluzioni', labelpad=15)
ax.set_title('CalenPIario - {}'.format(now), pad=15)
plt.savefig("calenPIarioStats_Problems.png")

url = 'https://www.rimosco.it/picalendar/index.php?a=highscore'
r = requests.get(url)
pical_highscore = BeautifulSoup(r.text, 'html.parser')
table = str(pical_highscore.find_all("table")[0])
table = table.replace("<table><tr><td>Punteggio</td><td>Nickname</td></tr><tr>","").replace("</tr></table>","")
table = [ [ i.replace('<td>','').replace('</td>','') for i in l.split("</td><td>") ] for l in table.split("</tr><tr>") ]

pmin = 0 # skip names below a minimal score
points = []
names = []
for point,name in table:
    if int(point)>pmin:
        points.append(int(point))
        names.append(name)
        
fig, ax = plt.subplots(figsize=(12,8),dpi=100)
plt.bar(names,points)
plt.xticks(range(len(names)), names, rotation='vertical')
fig.subplots_adjust(bottom=0.35)
ax.set_xlabel('Nome', labelpad=15)
ax.set_ylabel('Punteggio', labelpad=15)
ax.set_title('CalenPIario - {}'.format(now), pad=15)
plt.savefig("calenPIarioStats_Scores.png")

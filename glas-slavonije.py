# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import nltk
from fuzzywuzzy import fuzz
import string
import funkcije
from gradovi import GRADOVI
from compiler.ast import flatten
from time import sleep
import time

linkovi=[]

r = requests.get('http://www.glas-slavonije.hr/')
r.encoding = 'utf-8'
tekst = r.text
soup = BeautifulSoup(tekst)
clanak = soup.find("div", "col1").findAll("a") #flexslider - najnoviji clanci

for link in clanak:
    a = (link.get('href'))
    if a[:10] != "javascript" and a[:28] != "http://www.glas-slavonije.hr":
        if a[:5] == "http":
            a = "http://www.glas-slavonije.hr" + a
            if a not in linkovi:
                linkovi.append(a)

r = requests.get('http://www.glas-slavonije.hr/Novosti')
r.encoding = 'utf-8'
tekst= r.text
soup = BeautifulSoup(tekst)
clanak = soup.find("div", "col1").findAll("a") #flexslider - najnoviji clanci

for link in clanak:
    a = (link.get('href'))
    if a[:10] != "javascript" and a[:28] != "http://www.glas-slavonije.hr":    
        a = "http://www.glas-slavonije.hr" + a
        if a not in linkovi:
            linkovi.append(a)

r = requests.get('http://www.glas-slavonije.hr/Osijek')
r.encoding = 'utf-8'
tekst = r.text
soup = BeautifulSoup(tekst)
clanak = soup.find("div", "col1").findAll("a") #flexslider - najnoviji clanci

for link in clanak:
    a = (link.get('href'))
    if a[:10] != "javascript" and a[:28] != "http://www.glas-slavonije.hr":    
        a = "http://www.glas-slavonije.hr" + a
        if a not in linkovi:
            linkovi.append(a)
                 
r = requests.get('http://www.glas-slavonije.hr/Regija')
r.encoding = 'utf-8'
tekst = r.text
soup = BeautifulSoup(tekst)
clanak = soup.find("div", "col1").findAll("a") #flexslider - najnoviji clanci

for link in clanak:
    a = (link.get('href'))
    if a[:10] != "javascript" and a[:28] != "http://www.glas-slavonije.hr":    
        a = "http://www.glas-slavonije.hr" + a
        if a not in linkovi:
            linkovi.append(a)

num=len(linkovi)

print ""
print "----------" + str(num) + "----------"

file = open("glas-slavonije.txt", "r+")
stari_linkovi = []

for line in file:
    link = line.split(";")
    stari_linkovi.append(link[0])
file.close()
 
file2 = open("glas-slavonije.hr_bez_lokacije.txt", "r+")
for line in file2:
    bez = line.split(";")
    stari_linkovi.append(bez[0])
file2.close()   

new_file_list = []    

for link in linkovi:
    if not link in stari_linkovi:
        file = open("glas-slavonije.txt", "a")
        link = str(link)
        r = requests.get(link)
        r.encoding = 'utf-8'
        tekst = r.text
    
        li = []
        soup = BeautifulSoup(tekst)

        if soup.find("div","vijest-nadnas") != None:            
            nadnaslov = soup.find("div","vijest-nadnas").getText()
            nadnaslov = str(nadnaslov)
            nadnaslov = nadnaslov.title()
        
        if soup.find("div","vijest-naslov") != None:
            naslov = soup.find("div","vijest-naslov").getText()
            naslov = str(naslov)
        cijeli_naslov = naslov + " " + nadnaslov
        
        clanak = soup.find("div", "vijest-body").findAll("p")
        cisti_clanak = funkcije.ocisti_clanak(clanak)
        datum = soup.find("div","datum-objave").getText()
        datum = funkcije.uredi_datum(datum)

        li.append(link)
        li.extend(funkcije.nadji(GRADOVI,cisti_clanak))
        
        if len(li) < 2:
            cisti_clanak = cijeli_naslov + " " + cisti_clanak
            li.extend(funkcije.nadji_grad_jf(GRADOVI,cisti_clanak))    
            if len(li) >= 6:
                li = li[:7]
            li.sort(key=lambda x: x[1])
            li.reverse()
            li = flatten(li)
            if len(li) > 7:
                li = li[:7]
        
        if len(li)>1:
            if len(li) == 3:
                konacno = funkcije.nadji_sve(li)
            
            if len(li) == 5:
                li1 = li[:3]
                odg1 = funkcije.funkcije.nadji_sve(li1)

                li2 = [li[0],li[3],li[4]]
                odg2 = funkcije.nadji_sve(li2)

                lst = [odg1,odg2]
                if lst[0][2] > lst [1][2]:
                    konacno = lst[0]
                if lst[0][2] < lst [1][2]:
                    konacno = lst[1]
                if lst[0][2] == lst [1][2]:
                    konacno = lst[0]
                    konacno2 = lst[1]
                    konacno2 = ";".join(konacno2)                    
                    konacno2 = konacno2 + ";" + datum + "\n"
                    print konacno2
                    file.write(konacno2)

            if len(li) == 7:
                li1 = li[:3]
                odg1 = funkcije.nadji_sve(li1)
                
                li2 = [li[0],li[3],li[4]]
                odg2 = funkcije.nadji_sve(li2)             
                
                li3 = li
                li3.pop(1)
                li3.pop(1)
                li3.pop(1)
                li3.pop(1)
                odg3 = funkcije.nadji_sve(li3)                
                
                start = 0
                lst = [odg1,odg2, odg3]
                
                lst.sort(key=lambda x: x[2])
                lst.reverse()
                if lst[0][2] > lst[1][2]:
                    konacno = lst[0]
                if lst[0][2] == lst[1][2]:
                    konacno = lst[0]
                    konacno2 = lst[1]
                    konacno2 = ";".join(konacno2)                    
                    konacno2 = konacno2 + ";" + datum + "\n"
                    print konacno2
                    file.write(konacno2)

            konacno = ";".join(konacno)                    
            konacno = konacno + ";" + datum + "\n"
            print konacno
            file.write(konacno)
            file.close()

        else:
            file2 = open("glas-slavonije.hr_bez_lokacije.txt", "a")
            konacno = li[0] + ";" + datum + "\n"
            file2.write(konacno)
            file2.close()

        file.close()
        print "Waiting..."
        time.sleep(5)
 
    num -= 1
    print "----------" + str(num) + "----------"
    print""

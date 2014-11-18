# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import nltk
from fuzzywuzzy import fuzz
import string
import funkcije
from gradovi import GRADOVI
from shapely.geometry import Point
import pyproj
from compiler.ast import flatten
from time import sleep
import time

pHTRS96 = pyproj.Proj(init='EPSG:3765')
pWGS84 = pyproj.Proj(init='EPSG:4326')

r = requests.get('http://www.istranews.in/')
r.encoding = 'utf-8'
tekst= r.text

soup = BeautifulSoup(tekst)

linkovi=[]

clanak=soup.find("div", "flexslider").findAll("a") #flexslider - najnoviji clanci

for link in clanak:
    a=(link.get('href'))
    a="http://www.istranews.in"+a
    if a not in linkovi:
        linkovi.append(a)

clanak=soup.find("div", "outerwide").findAll("a") #outerwide-ostali clanci

for link in clanak:
    a=(link.get('href'))
    a="http://www.istranews.in"+a
    if a not in linkovi:
        linkovi.append(a)

clanak=soup.find("div", "slider2").findAll("a") #outerwide-ostali clanci

for link in clanak:
    a=(link.get('href'))
    a="http://www.istranews.in"+a
    if a not in linkovi:
        linkovi.append(a)

file = open("istranews.txt", "r")
stari_linkovi=[]
for line in file:
    link = line.split(";")
    stari_linkovi.append(link[0])
file.close()

file2 = open("istranews.in_bez_lokacije.txt", "r")
for line in file2:
    link = line.split(";")
    stari_linkovi.append(link[0])
file2.close()
   
new_file_list=[] 
   
for link in linkovi:
    
    if link not in stari_linkovi:
        file = open("istranews.txt", "a")
        r=requests.get(link)
        r.encoding = 'utf-8'
        tekst = r.text
       
        li=[]
        soup = BeautifulSoup(tekst)
        naslov = soup.find("h6", "title").getText()#.findAll("p")
        naslov = str(naslov)
        clanak = soup.find("div", "article_text").findAll("p")
        datum = soup.find("span", "meta").getText()
        datum = funkcije.uredi_datum(datum)
        datum = datum[:11]
        novi_datum = ""
        for slovo in datum:
            if slovo != " " and slovo != ":":
                novi_datum += slovo
            else:
                pass
        datum = novi_datum

        cisti_clanak = funkcije.ocisti_clanak(clanak)
        li.append(link)
        
        li.extend(funkcije.nadji(GRADOVI,cisti_clanak))
        
        if len(li)<2:
            cisti_clanak=naslov+" "+cisti_clanak
            li.extend(funkcije.nadji_grad_jf(GRADOVI,cisti_clanak))
            if len(li) >= 6:
                li = li[:7]
            li.sort(key=lambda x: x[1])
            li.reverse()
            li = flatten(li)
            if len(li) > 7:
                li = li[:7]

        kontrola=[]
        kontrola.append(link)
        lokacija=soup.find("span", "meta").findAll('a')
        for link1 in lokacija:
            if link1.get('href')[:8]=="/gradovi":
                a=link1.getText()
                if a[-1]==".":
                    a= a[:-1]

                kontrola.append(a)
                kontrola.append(3.0)
        
        if len(li)>2 and len(kontrola)>2:
            if kontrola[1] in li:
                lst = []
                lst.append(li[0])
                lst.append(li[li.index(kontrola[1])])  #index na kojem je grad
                lst.append(li[li.index(kontrola[1])+1])  #index na kojem je koedicijent
            
                rez = funkcije.dodijeli_koordinate(lst) 
                za_tocku1=[]
                for element in rez.split(';'):
                    za_tocku1.append(element)
                
                rez2 = funkcije.dodijeli_koordinate(kontrola)
                
                za_tocku2=[]
                for element in rez2.split(';'):
                    za_tocku2.append(element)
                
                lat1 = float(za_tocku1[3])
                lon1 = float(za_tocku1[4])
                       
                lat2 = za_tocku2[3]
                lon2 = za_tocku2[4]
                
                E1, N1 = pyproj.transform(pWGS84, pHTRS96, lon1, lat1)
                E2, N2 = pyproj.transform(pWGS84, pHTRS96, lon2, lat2)
        
                tocka = Point (E1, N1)
                tocka_k = Point (E2, N2)        
                
                udaljenost = tocka.distance(tocka_k)

                if udaljenost <= 25000 :#25km
                    n=float(za_tocku1[2])
                    n+=1
                    za_tocku1[2]=str(n)
                    li[li.index(kontrola[1])+1] = str(n)

                else:
                    li.append(za_tocku2[1])
                    li.append(float(za_tocku2[2]))

            else:
                rez2 = funkcije.dodijeli_koordinate(kontrola)
                za_tocku2=[]
                for element in rez2.split(';'):
                    za_tocku2.append(element)
                li.append(za_tocku2[1])
                li.append(float(za_tocku2[2]))
                
        elif len(li)<2 and len(kontrola)>2:  
            rez2 = funkcije.dodijeli_koordinate(kontrola)
            za_tocku2=[]
            for element in rez2.split(';'):
                za_tocku2.append(element)
            li.append(za_tocku2[1])
            li.append(float(za_tocku2[2]))
        
        lista = []
        a = 1
        lista.append(li[0])
        while a < len(li)-1:
            lista.append([li[a],li[a+1]])
            a+=2
        
        lista.sort(key=lambda x: x[1])
        lista.reverse()
        lista = flatten(lista)
        
        li = lista
        
        if len(li)>1:
            if len(li) == 3:
                konacno = funkcije.nadji_sve(li)
            
            if len(li) == 5:
                li1 = li[:3]
                odg1 = funkcije.funkcije.nadji_sve(li1)

                li2 = [li[0],li[3],li[4]]
                odg2 = funkcije.nadji_sve(li2)

                start = 0
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

            if len(li) >= 7:
                li = li[:7]
                li1 = li[:3]
                odg1 = funkcije.nadji_sve(li1)
                
                li2 = [li[0],li[3],li[4]]
                odg2 = funkcije.nadji_sve(li2)            
                
                li3 = [li[0],li[5],li[6]]
                odg3 = funkcije.nadji_sve(li3)
                
                start = 0
                lst = [odg1, odg2, odg3]
                
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
              
            print konacno
            konacno = ";".join(konacno)                    
            konacno = konacno + ";" + datum + "\n"
            file.write(konacno)     

        else:
            file2 = open("istranews.in_bez_lokacije.txt", "a")
            konacno = li[0] + ";" + datum + "\n"
            file2.write(konacno)
            file2.close()
            
        file.close()
        time.sleep(2)

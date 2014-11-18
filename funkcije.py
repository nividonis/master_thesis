# -*- coding: utf-8 -*-
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from gradovi import GRADOVI
import funkcije

#clanak je s tagovima (<p>); type lista
#novi je clanak bez tagova; type string
#novi2 je lista, svaka recenica je novi clan

def ocisti_clanak(clanak):
    novi=""
    for tekst in clanak:
        for rijec in tekst.text.split(' '):
            #print rijec
            rijec=" "+rijec+" "
            rijec=str(rijec.strip(' ').strip(','))
            novi+=" "+rijec+" "
            
    novi2=sent_tokenize(novi)
    
    cisti_clanak=""
    for recenica in novi2:
        novi3 = word_tokenize(recenica)
        for element in novi3:
            if element == ".":
                novi3.remove(".")
            if element == "!":
                novi3.remove("!")
            if element == "?":
                novi3.remove("?")
            if element == "(":
                novi3.remove("(")
            if element == ")":
                novi3.remove(")")
            if element == ":":
                novi3.remove(":")
        novi3=" ".join(novi3)
        cisti_clanak=cisti_clanak+" "+novi3
    return cisti_clanak


def usporedi_rijeci(s1,s2):
    """
    s1 je grad iz popisa
    s2 je potencijalni grad iz clanka
    """
    l1=[]
    l2=[]
    for rijec in s1.split(" "):
        l1.append(rijec)
    for rijec in s2.split(" "):
        l2.append(rijec)  
    if len(l1)==len(l2):    
        if len(l1)==1:
            if len(l1[0])<=3:
                if l1[0]== l2[0][:(len(l1[0]))]:
                    if len(l1[0])<=len(l2[0]):
                        return True        
            elif len(l1[0])>3:            
                if l1[0][:-2] == l2[0][:(len(l1[0])-2)] :
                    if len(l1[0]) <= len(l2[0]) :
                        return True
                else:
                    pass
        if len(l1)==2:
            if l1[0][:-2]== l2[0][:(len(l1[0])-2)]:
                if l1[1][:-2]== l2[1][:(len(l1[1])-2)]:
                    return True
                else:
                    pass
        if len(l1)==3:
            if l1[0][:-2]== l2[0][:(len(l1[0])-2)]:
                if l1[1][:-2]== l2[1][:(len(l1[1])-2)]:
                    if l1[2][:-2]== l2[2][:(len(l1[2])-2)]:
                        return True
                    else:
                        pass
        if len(l1)==4:
            if l1[0][:-2]== l2[0][:(len(l1[0])-2)]:
                if l1[1][:-2]== l2[1][:(len(l1[1])-2)]:
                    if l1[2][:-2]== l2[2][:(len(l1[2])-2)]:
                        if l1[3][:-2]== l2[3][:(len(l1[3])-2)]:
                            return True
                        else:
                            pass
   

def dodijeli_koordinate(l):
    s=""
    s1=""
    r=[]
    for grad in GRADOVI.keys():
        if len(l)<2:
            pass
        elif l[1]==grad and len(l)==3:
            print l.extend(GRADOVI.get(grad))
            s = l[0]+";"+l[1]+";"+str(l[2])+";"+str(l[3])+";"+str(l[4])
            return s
        elif len(l)==5:
            if l[1]==grad:             
                l1=l[:3]
                l1.extend(GRADOVI.get(grad))
                s = l1[0]+";"+l1[1]+";"+str(l1[2])+";"+str(l1[3])+";"+str(l1[4])

            if l[3]==grad:
                l2=[l[0],l[3],l[4]]
                l2.extend(GRADOVI.get(grad))
                s1 = l2[0]+";"+l2[1]+";"+str(l2[2])+";"+str(l2[3])+";"+str(l2[4])
    r=[s,s1]
    if s!="" and s1!="":
        return r

def nadji(gradovi,cisti_clanak):
    from gradovi import GRADOVI
    from fuzzywuzzy import fuzz
    tekst=""
    l=[]
    s=cisti_clanak[:40]
    if " & nbsp ; " in s:
        s=s.replace("& nbsp ;","")
    if s[0]==" ":
        s=s[1:]
    for rijec in s.split("-"):
        if rijec.isupper():
            tekst=rijec
    for rijec in s.split("–"):
        if rijec.isupper():
            tekst=rijec
    for rijec in tekst.split('/'):
        if rijec.isupper():
            rijec=unicode(rijec)
            if rijec[0]==" ":
                rijec=rijec[1:]
            while not rijec[-1].isalpha():
                if rijec[-1]!="Č" and rijec[-1]!="Ć" and rijec[-1]!="Đ" and rijec[-1]!="Š" and rijec[-1]!="Ž":
                    rijec=rijec[:-1]
            if rijec!="I" and rijec!="A" and rijec!="E" and rijec != "O" and rijec != "U":
                rijec=rijec.title()
                rijec=str(rijec)
                
                for grad in GRADOVI.keys():
                    if grad==rijec:
                        l.append(grad)
                        l.append("5.0")
                        
    if len(l)<2:
        for rijec in tekst.split(' '):
            if rijec.isupper():
                rijec=unicode(rijec)
                if rijec[0]==" ":
                    rijec=rijec[1:]
                    while not rijec[-1].isalpha():
                        if rijec[-1]!="Č" and rijec[-1]!="Ć" and rijec[-1]!="Đ" and rijec[-1]!="Š" and rijec[-1]!="Ž":
                            rijec=rijec[:-1]
                        if rijec!="I" and rijec!="A" and rijec!="E" and rijec != "O" and rijec != "U":
                            rijec=rijec.title()
                            rijec=str(rijec)
                            
                            for grad in GRADOVI.keys():
                                if grad==rijec:
                                    l.append(grad)
                                    l.append("5.0")
    return l


def uredi_datum(datum):
    from datetime import datetime

    now=datetime.now()
    y=now.year
    m=now.month
    d=now.day
    h=now.hour
    mi=now.minute
    d=str(d)
    if len(d)==1:
        d="0"+d
    if len(str(m))==1:
        m="0"+str(m)
    danas=str(d)+"."+str(m)+"."+str(y)+"."
    datum=str(datum)
    if datum[-3:]=="min":
        danas_sati=int(h)+float(mi)/60
        if "Objavljeno" in datum:
            datum=datum.replace("Objavljeno","")
        if ":" in datum:
            datum=datum.replace(":","")
        if "prije" in datum:
            datum=datum.replace("prije","")
        if "min" in datum:
            datum=datum.replace("min","")
        if "h" in datum:
            datum=datum.replace("h","")
        if "i" in datum:
            datum=datum.replace("i","")
            
        while datum[0]==" ":
            datum=datum[1:]
        while datum[-1]==" ":
            datum=datum[:-1]
            
        sati=datum[:2]
        minute=datum[-2:]
        clanak_sati=int(sati)+float(minute)/60
        if clanak_sati<danas_sati:
            datum=danas
        else:
            d=int(d)-1
            datum=str(d)+"."+m+"."+str(y)+"."
   
        datum=danas
    else:
        if datum[-1]==".":
            datum=datum[:-1]
        if "Objavljeno" in datum:
            datum=datum.replace("Objavljeno","")
        if ":" in datum:
            datum=datum.replace(":","")
        while datum[0]==" ":
            datum=datum[1:]
        y=datum[-4:]+"."
        datum=datum[:-4]
        d=datum[:3]
        if d[-1]==" ":
            d=d[:-1]
            if len(d)<3:
                d="0"+d
        m=datum[3:]
        if m[0]==" ":
            m=m[1:]
        if m[-1]==" ":
            m=m[:-1]
        if m[-1]==",":
            m=m[:-1]
        
        if m=="siječanj" or m=="siječnja":
            m="01."
        if m=="veljača" or m=="veljače":
            m="02."
        if m=="ožujak" or m=="ožujka":
            m="03."
        if m=="travanj" or m=="travnja":
            m="04."
        if m=="svibanj" or m=="svibnja":
            m="05."
        if m=="lipanj" or m=="lipnja":
            m="06."
        if m=="srpanj" or m=="srpnja":
            m="07."
        if m=="kolovoz" or m=="kolovoza":
            m="08."
        if m=="rujan" or m=="rujna":
            m="09."
        if m=="listopad" or m=="listopada":
            m="10."
        if m=="studeni" or m=="studenog":
            m="11."
        if m=="prosinac" or m=="prosinca":
            m="12."

        datum=d+m+y
    return datum


def usporedi_lokacije(li):
    from geopy.geocoders import GoogleV3
    geolocator = GoogleV3()
    from shapely.geometry import Point
    import pyproj
    
    if len(li)>1:
        lat1=0
        lon1=0
        lat2=0
        lon2=0
        if li[-1] == 0 or li[-1] == "0":
            cc=li[1]+", Croatia"
        else:
            cc=li[1]+", Croatia"
        if geolocator.geocode(cc)!=None:
            
            address, (latitude, longitude) = geolocator.geocode(cc)
            odg=(address, latitude, longitude)
            li.append(str(odg))
            
            pHTRS96 = pyproj.Proj(init='EPSG:3765')
            pWGS84 = pyproj.Proj(init='EPSG:4326')
                    
            za_tocku1 = li#[:8]           
            
            lat1 = float(za_tocku1[3])
            lon1 = float(za_tocku1[4])
                        
            lat2 = odg[1]
            lon2 = odg[2]
                        
            E1, N1 = pyproj.transform(pWGS84, pHTRS96, lon1, lat1)
            E2, N2 = pyproj.transform(pWGS84, pHTRS96, lon2, lat2)
                
            tocka = Point (E1, N1)
                
            tocka_k = Point (E2, N2)        
                        
            udaljenost = tocka.distance(tocka_k)/1000
            udaljenost=round(udaljenost,4)
            za_tocku1.append(str(udaljenost))
            
            if udaljenost <= 25 :#25km
                n=float(za_tocku1[2])
                n+=0.5
                za_tocku1[2]=str(n)
                konacno = za_tocku1                
                return konacno
                
            else:
                konacno = za_tocku1
                n=float(za_tocku1[2])
                n-=0.5
                za_tocku1[2]=str(n)
                return konacno
                
        else:
            li.append("-")
            li.append("-")
            konacno = li
            return konacno



def nadji_zupaniju(geoname):  #lista s koordinatama iz geonamesa
    from shapely.geometry import Polygon, Point
    from shapely.wkb import loads
    from osgeo import ogr
    from sys import maxint
    
    polyIN = ogr.Open("zupanije_wgs84_poligoni.shp")
    polyLayer = polyIN.GetLayerByName("zupanije_wgs84_poligoni")
    polygons = []
    polygon = polyLayer.GetNextFeature()
    while polygon is not None:
        polygons.append(polygon)
        polygon = polyLayer.GetNextFeature()
    polyIN.Destroy()
    point = Point(float(geoname[4]), float(geoname[3]))
    
    for i in range(len(polygons)):
        geom = loads(polygons[i].GetGeometryRef().ExportToWkb())     
        if point.within(geom):
            id_zup = polygons[i].zup_rb
        else:
            id_zup = 0
            
    if id_zup == 0:
        dist = maxint
        for j in range(len(polygons)):
            geom = loads(polygons[j].GetGeometryRef().ExportToWkb())
            udaljenost = point.distance(geom)
            if udaljenost < dist:
                dist = udaljenost
                id_zup = polygons[j].zup_rb
                   
    geoname.append(str(id_zup))
    geoname.append(str(dist))
    
    return geoname
    
    
def nadji_postanski_broj(geoname):
    csvIN = open('MjestaRH1.csv', 'rb')
    zup_dict = {}
    for line in csvIN:
        split_line = line.split(';')
        if split_line[0] != 'Broj_pu':
            key = str(split_line[-1][:-1])
            data = [split_line[1], split_line[0]]
            data2 = [split_line[3], split_line[0]]
    
            if zup_dict.has_key(key):
                if data not in zup_dict[key]:
                    zup_dict[key].append(data)
                if data2 not in zup_dict[key]:
                    zup_dict[key].append(data2)
            else:
                key = str(split_line[-1][:-1])		
                zup_dict[key] = [data]
                zup_dict[key] = [data2]

    id_zup=geoname[-2]
    if id_zup == "21":
        id_zup = "1"
    postanski_broj = "0"
    if id_zup != 0 and id_zup != "0":
        for i in range (len(zup_dict[id_zup])):
            if zup_dict[id_zup][i][0]==geoname[1]:
                postanski_broj = zup_dict[id_zup][i][1]
            i-=1
    elif id_zup == 0 or id_zup == "0":
        postanski_broj = "0"
    geoname.append(postanski_broj)  
    if postanski_broj != "0":
        geoname[2]=str(float(geoname[2])+0.5)
    return geoname
    
def nadji_sve(li):
    if len(li)>1:
        geoname = funkcije.dodijeli_koordinate(li)
        geoname = geoname.split(";")
        geoname = funkcije.nadji_zupaniju(geoname)
        geoname = funkcije.nadji_postanski_broj(geoname)
        konacno = funkcije.usporedi_lokacije(geoname)
        return konacno
            
    
def nadji_grad_jf(gradovi,cisti_clanak): 
    from gradovi import GRADOVI
    import jellyfish
    clanak=[]
    l=[]
    lista_gradova=[]
    brojac=0    
    for rijec in cisti_clanak.split(' '): 
        brojac+=1
        
    for rijec in cisti_clanak.split(" "):
        clanak.append(rijec)
        
    for i in range(0,len(clanak)-4):

        st=clanak[i]+" "+clanak[i+1] +" "+clanak[i+2] +" "+clanak[i+3] +" "+clanak[i+4]
        if not clanak[i].islower() and not clanak[i+4].islower():
            for grad in GRADOVI:
                razlika = jellyfish.jaro_distance(grad, st)
                bodovi=razlika*0.7
                if razlika>=0.9:
                    if usporedi_rijeci(grad,st)==True:
                        if i/float(brojac)<0.33:
                            b=0.3
                        elif i/float(brojac)<0.66:
                            b=0.2
                        else:
                            b=0.1   
                        suma = bodovi + b
                        if suma > 0.75:
                            for x in range(0,len(l)):
                                if grad == l[x][0]:
                                    if suma > l[x][1]:
                                        l[x][1] = suma     
                                    l[x][1] += 0.025
                            if grad not in lista_gradova:
                                l.append([grad,suma])   
                                lista_gradova.append(grad)
  
        st=clanak[i]+" "+clanak[i+1] +" "+clanak[i+2] +" "+clanak[i+3]
        if not clanak[i].islower() and not clanak[i+3].islower():
            for grad in GRADOVI:
                razlika = jellyfish.jaro_distance(grad, st)
                bodovi=razlika*0.7
                if razlika>=0.9:
                    if usporedi_rijeci(grad,st)==True:
                        if i/float(brojac)<0.33:
                            b=0.3
                        elif i/float(brojac)<0.66:
                            b=0.2   
                        else:
                            b=0.1    
                        suma = bodovi + b
                        if suma > 0.75:
                            for x in range(0,len(l)):
                                if grad == l[x][0]:
                                    if suma > l[x][1]:
                                        l[x][1] = suma   
                                    l[x][1] += 0.1
                            if grad not in lista_gradova:
                                l.append([grad,suma])
                                lista_gradova.append(grad)

        st=clanak[i]+" "+clanak[i+1] +" "+clanak[i+2]
        if not clanak[i].islower() and not clanak[i+2].islower():
            for grad in GRADOVI:
                razlika = jellyfish.jaro_distance(grad, st)
                bodovi=razlika*0.7
                if razlika>=0.9:
                    if usporedi_rijeci(grad,st)==True:
                        if i/float(brojac)<0.33:
                            b=0.3
                        elif i/float(brojac)<0.66:
                            b=0.2   
                        else:
                            b=0.1  
                        suma = bodovi + b
                        if suma > 0.75:
                            for x in range(0,len(l)):
                                if grad == l[x][0]:
                                    if suma > l[x][1]:
                                        l[x][1] = suma   
                                    l[x][1] += 0.025
                            if grad not in lista_gradova:
                                l.append([grad,suma])
                                lista_gradova.append(grad)
 
        st=clanak[i]+" "+clanak[i+1]
        if not clanak[i].islower() and not clanak[i+1].islower():
            for grad in GRADOVI:
                razlika = jellyfish.jaro_distance(grad, st)
                bodovi=razlika*0.7
                if razlika>=0.9:
                    if usporedi_rijeci(grad,st)==True:
                        if i/float(brojac)<0.33:
                            b=0.3
                        elif i/float(brojac)<0.66:
                            b=0.2   
                        else:
                            b=0.1 
                        suma = bodovi + b
                        if suma > 0.75:
                            for x in range(0,len(l)):
                                if grad == l[x][0]:
                                    if suma > l[x][1]:
                                        l[x][1] = suma   
                                    l[x][1] += 0.1
                            if grad not in lista_gradova:
                                l.append([grad,suma])
                                lista_gradova.append(grad)

        st=clanak[i]
        if not st in rijeci:
            if not st.islower() or st[0]!="Č" or st[0]!="Ć" or st[0]!="Đ" or st[0]!="Š" or st[0]!="Ž":
                for grad in GRADOVI:
                    razlika = jellyfish.jaro_distance(grad, st)
                    bodovi=razlika*0.7
                    if razlika>=0.9:
                        if usporedi_rijeci(grad,st)==True:
                            if i/float(brojac)<0.33:
                                b=0.3
                            elif i/float(brojac)<0.66:
                                b=0.2
                            else:
                                b=0.1
                            suma = bodovi + b
                            if suma > 0.75:
                                for x in range(0,len(l)):
                                    if grad == l[x][0]:
                                        if suma > l[x][1]:
                                            l[x][1] = suma  
                                        l[x][1] += 0.025
                                if grad not in lista_gradova:
                                    l.append([grad,suma])
                                    lista_gradova.append(grad)
                                    
    print "gradovi", lista_gradova                   
    return l

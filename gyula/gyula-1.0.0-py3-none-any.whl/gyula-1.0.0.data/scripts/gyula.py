#!python

import os
import re
import sys
import json
import requests
import datetime
import random
from bs4 import BeautifulSoup

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def bpm():
    
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
 
    r = requests.post("https://songbpm.com/api/searches", headers=headers, json={'query':input("Keresés: ")})

    songs = requests.get("https://songbpm.com/_next/data/Obrt0Ok0kZXsEgtUAlCqI/searches/"+r.json()["id"]+".json?id="+r.json()["id"], headers=headers)
    data = songs.json()["pageProps"]["search"]["searchSongs"][0]["song"]["data"]

    # song title
    print(data["name"])

    # artist(s)
    for i in range(len(data["artists"])):
        print (data["artists"][i]["name"])

    # tempo
    
    print(songs.json()["pageProps"]["search"]["searchSongs"][0]["song"]["tempo"])

akasztourl = "https://raw.githubusercontent.com/ShrekhavingabadDay/osszes_magyar_szo/main/osszes_magyar_szo.txt"
    
osszetett = ['ly', 'sz', 'zs', 'ty', 'gy', 'ny', 'cs', 'dzs', 'dz']

rajz = {

	0 : '',
	1 : '/--\\',
	2 : ' |/--\n |\n |\n |\n/--\\',
	3 : ' |/--:\n |\n |\n |\n/--\\',
	4 : ' |/--:\n |   O\n |\n |\n/--\\',
	5 : ' |/--:\n |   O\n |   |\n |\n/--\\',
	6 : ' |/--:\n |   O\n |  \|\n |\n/--\\',
	7 : ' |/--:\n |   O\n |  \|/\n |\n/--\\',
	8 : ' |/--:\n |   O\n |  \|/\n |  /\n/--\\',
	9 : ' |/--:\n |   O\n |  \|/\n |  / \\\n/--\\',


}

# |/--:
# |   O
# |  \|/
# |  / \
#/--\

def get_word():
	try:
		r = requests.get(akasztourl)
	except:
		return False

	szavak = r.text

	return random.choice(szavak.strip().split())

def nyert(szo, helyzet):
	for i in range(len(szo)):
		if szo[i] != helyzet[i]:
			return False
	return True

def akasztofa():

	def vege(nyert):
	
		if nyert:
			print('Azosztigen!\n')
		else:
			print(szo)	
			print('Fel let akasztva a kiscsávó :D\n')
			
		megegyet = input('Még egyet?[i/n]>>')
		
		if megegyet == '' or megegyet == 'i':
			return (get_word(), 0, [], False)
		
		else:
			return (None, None, None, True)
		
	veszit = len(rajz)-1
		
	nemtalalt = 0
	
	ajjaj = []

	szo = get_word()
	
	jatekvege = False
	
	helyzet = ['-']*len(szo)
	
	while not jatekvege:
	
		os.system('clear')
		print(rajz[nemtalalt])
		print(''.join(helyzet))
		print(', '.join(ajjaj))
		
		betu = input('>>')
		
		if betu == '/':
			system('clear')
			return
		
		talalt = False
		
		if len(betu)>0:
		
			if len(betu) == 1:
				for i,c in enumerate(szo):
					if c == betu:
					
						if i<len(szo)-1 and szo[i]+szo[i+1] in osszetett:
							continue
							
						helyzet[i] = betu
						talalt = True
						
			else:
			
				if szo == betu:
					helyzet = szo.split()
					os.system('clear')
					print(rajz[nemtalalt])
					print(''.join(helyzet))
					szo, nemtalalt, ajjaj, jatekvege = vege(True)
					if szo:
						helyzet = ['-']*len(szo)
					continue
					
				else:
					hossz = len(betu)
					n = len(szo)-hossz+1
					for i in range(0,n):
						if szo[i:i+hossz] == betu:
							for j in range(hossz):
								helyzet[i+j] = betu[j]
							talalt = True
					
				
			if talalt:
				if nyert(szo, helyzet):
					helyzet = szo.split()
					os.system('clear')
					print(rajz[nemtalalt])
					print(''.join(helyzet))
					szo, nemtalalt, ajjaj, jatekvege = vege(True)
					if szo:
						helyzet = ['-']*len(szo)
				
			else:
			
				if betu not in ajjaj:
					ajjaj += [betu]
					nemtalalt+=1
				
				if nemtalalt == veszit:
					os.system('clear')
					print(rajz[nemtalalt])
					print(''.join(helyzet))
					szo, nemtalalt, ajjaj, jatekvege = vege(False)
					if szo:
						helyzet = ['-']*len(szo)
nt = '--Nincs találat--'

base_url = "https://topszotar.hu"

def idegennyelv(r):
		
	leves = BeautifulSoup(r.text, 'html.parser')
	
	tags = [tag.find('a') for tag in leves.find_all('span', {'class':"sense"})]

	return '\n'.join("- "+tag.text.strip() for tag in tags)

def szotar(option, value):

	if re.match("magyar[-]?n[eé]met", option) or option=="mn":

		r = requests.get(base_url+"/magyarnemet/"+value)
		
		valasz = idegennyelv(r)
		
		if valasz == '':
			return nt
		
		return valasz
		
	
	elif re.match("n[eé]met[-]?magyar", option) or option == "nm":
	
		r = requests.get(base_url+"/nemetmagyar/"+value)
		
		valasz = idegennyelv(r)
		
		if valasz == '':
			return nt
		
		return valasz
		
	elif re.match("angol[-]?magyar", option) or option == "am":
	
		r = requests.get(base_url+"/angolmagyar/"+value)
		
		valasz = idegennyelv(r)
		
		if valasz == '':
			return nt
		
		return valasz
		
	elif re.match("magyar[-]?angol", option) or option == "ma":
	
		r = requests.get(base_url+"/magyarangol/"+value)
		
		valasz = idegennyelv(r)
		
		if valasz == '':
			return nt
		
		return valasz
		
	elif option == "szinonima" or option == "sz":
	
		r = requests.get(base_url+"/szinonima-szotar/"+value)
		
		soup = BeautifulSoup(r.text, 'html.parser')
		
		try:
			return soup.find_all('div', {'class':'sense'})[0].text.strip()
		except:
			return nt
			
	elif option == "idegen" or option == "i":
	
		r = requests.get(base_url+"/idegen-szavak/"+value)
		
		soup = BeautifulSoup(r.text, 'html.parser')

		try:
			return ', '.join(
		tag.text.strip() for tag in soup.find('h1', {'class':'headword headword1'}).parent.find_all('li', {'class':None}))
		except:
			return nt
def elorejelzes(hely):

	r = requests.get("http://beepulo.idokep.hu/futar/"+hely)

	soup = BeautifulSoup(r.text, 'html.parser')

	mind = ([tag.get('onmouseover') for tag in soup.find_all('img') if tag.get('onmouseover')]+[tag.get('onmouseover') for tag in soup.find_all('div') if tag.get('onmouseover')])

	p = re.compile("Tip\('<b>(.*)<\/b><br[\/]?>(.*)\. '\)")

	d = {}

	for egy in mind:
		
		result = p.search(egy)
		
		date = result.group(2)
		
		if date not in d:
			d[date] = []
			
		d[date].append(result.group(1))

	output = 'Gyula az időjárást a https://www.idokep.hu segítségével tudja megmondani.\n'

	for key in d:
	
		output += key+'\n'
		
		for data in d[key]:
			output+= ('\t-'+data+'\n')
			
	return output


def helyese(szo):
	response = requests.post("https://helyesiras.mta.hu/helyesiras/default/suggest", files=
	{"word":(None,szo), 
	"_formkey":(None, "2f130010-f799-4115-b89f-5ba01dd88b2c"),
	"_formname":(None, "default")},
	verify=False
	)

	leves = BeautifulSoup(response.text, 'html.parser')

	result = leves.find('ul', {'class':'result'})

	if result.find('b').text == 'helyes':
		return('HELYES!')
	elif result.find('span', {'class':'suggest_list'}):
		return('Esetleg ezek valamelyikére gondoltál?\n --'+result.find('span', {'class':'suggest_list'}).text)
	else:
		return('Helytelen!')
		
def lotto():
    r = requests.get('http://www.lottoszamok.net/otoslotto/')

    soup = BeautifulSoup(r.text, 'html.parser')

    return(''.join(soup.find('ul', {'class':'fli-list'}).find('li').find('h2').find('strong').text.strip().split()[:-2])+'\n'+soup.find('li', {'class':'szamok_nagy'}).text.strip())
meneturl = 'https://menetrendek.hu/menetrend/interface/index.php'

def mai_datum():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")

def holnapi_datum():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")

def ora_perc():
    now = datetime.datetime.now()
    return now.strftime("%H:%M").split(":")

megallojson = {
    "func":"getStationOrAddrByText",
    
    "params":{
        "inputText":"Budapest",
        "searchIn":["stations"],
        "searchDate":mai_datum(),
        "maxResults":30,
        "networks":[1,2,3,10,11,12,13,14,24],
        "currentLang":"hu"
    }
}

korlatszotar = {

    'i':0,
    'n':1

}

keresojson = {
"func":"getRoutes",
"params":{
    "networks":[1,2,3,10,11,12,13,14,24],
    
    "datum":None,
    
    "hour":None,
    "min":None,
    
    "honnan":None,
    "honnan_eovx":None,
    "honnan_eovy":None,
    "honnan_ls_id":None,
    "honnan_settlement_id":None,
    "honnan_site_code":None,
    "honnan_zoom":None,
    
    "hova":None,
    "hova_eovx":None,
    "hova_eovy":None,
    "hova_ls_id":None,
    "hova_settlement_id":None,
    "hova_site_code":None,
    "hova_zoom":None,
    
    "ind_stype":"megallo",
    "keresztul_stype":"megallo",
    "maxatszallas":"5",
    "maxvar":"240",
    "maxwalk":"700",
    
    "napszak":3, #ezt nem vágom, olyan, mintha nem számítana 
    "naptipus":None, # 0 - időkorlátozó | 1 - idő nem számít
    
    "odavissza":0,
    "preferencia":"0",
    "rendezes":"1",
    "submitted":1,
    "talalatok":1,
    "target":0,
    "utirany":"oda",
    "var":"0",
    "erk_stype":"megallo",
    "ext_settings":"block",
    "filtering":0,
    "helyi":"No"
    }
}

def kereses(honnan, hova, datum, idolista, korlat):
    keresojson["params"]["honnan"] = honnan["lsname"]
    keresojson["params"]["honnan_eovx"] = honnan["eovx"]
    keresojson["params"]["honnan_eovy"] = honnan["eovy"]
    keresojson["params"]["honnan_ls_id"] = honnan["ls_id"]
    keresojson["params"]["honnan_settlement_id"] = honnan["settlement_id"]
    keresojson["params"]["honnan_site_code"] = honnan["site_code"]
    keresojson["params"]["honnan_zoom"] = honnan["zoom"]
    keresojson["params"]["hova"] = hova["lsname"]
    keresojson["params"]["hova_eovx"] = hova["eovx"]
    keresojson["params"]["hova_eovy"] = hova["eovy"]
    keresojson["params"]["hova_ls_id"] = hova["ls_id"]
    keresojson["params"]["hova_settlement_id"] = hova["settlement_id"]
    keresojson["params"]["hova_site_code"] = hova["site_code"]
    keresojson["params"]["hova_zoom"] = hova["zoom"]
    keresojson["params"]["datum"] = datum
    keresojson["params"]["hour"] = idolista[0]
    keresojson["params"]["min"] = idolista[1]
    keresojson["params"]["naptipus"] = korlat

def menetrend():
    hon = input('Honnan?>>')

    megallojson["params"]["inputText"] = hon

    print('Feldolgozás folyamatban...')
    
    try:
        honnan = requests.post(meneturl, json=megallojson).json()["results"][0]
    except:
        print("Ismeretlen állomás!")
        return
    #--------------------------------------------------------------#

    hov = input('Hova?>>')

    megallojson["params"]["inputText"] = hov

    print('Feldolgozás folyamatban...')

    try:
        hova = requests.post(meneturl, json=megallojson).json()["results"][0]
    except:
        print('Nincs ilyen célállomás!')
        return
    #--------------------------------------------------------------#

    korlat = input('Időkorlát?[i/n]>>')

    if korlat not in 'in':
        print("Érvénytelen!")
        return

    if korlat == 'i':

        idopont = input('Időpont(éééé-hh-nn/ma/holnap,óó:pp/most)>>')
        
        if ',' not in idopont:
            print("Érvénytelen időpont!")
            return

        spli = idopont.split(',')

        datum = spli[0]

        if datum == 'ma':
            datum = mai_datum()

        elif datum == 'holnap':
            datum = holnapi_datum()    
         
        idopont = spli[1]

        if idopont == "most":
            idolista = ora_perc()
        else:
            if ':' not in idopont:
                print("Érvénytelen időformátum!")
                return
            else:
                idolista = idopont.split(':')

        
    else:
        datum = mai_datum()
        idolista = ora_perc()
        
    kereses(honnan, hova, datum, idolista, korlatszotar[korlat])

    try:
        talalatok = (requests.post(url, json=keresojson).json())["results"]["talalatok"]
    except:
        print("Nincs találat!")
        return

    for jarat in talalatok:
        print("\n")
        print(talalatok[jarat]["jaratinfok"]['0']["vonalnev"])
        print(talalatok[jarat]["indulasi_hely"]+"-"+talalatok[jarat]["erkezesi_hely"])
        print("Indul: "+talalatok[jarat]["indulasi_ido"]+"\tÉrkezik: "+talalatok[jarat]["erkezesi_ido"])
        #print("Út időtartama: "+talalatok[jarat]["jaratinfok"]['0']["osszido"])
        print("Jegyárak:")
        print("\t-teljes: "+str(talalatok[jarat]["jaratinfok"]['0']["fare"]))
        print("\t-ötvenszázalékos: "+str(talalatok[jarat]["jaratinfok"]['0']["fare_50_percent"]))
        print("\t-kilencvenszázalékos: "+str(talalatok[jarat]["jaratinfok"]['0']["fare_90_percent"]))
        print("\n")
adat = {

    "valtasmod" : "kozep",
    "amount" : "420",
    "valuta_from" : "HUF",
    "valuta_to" : "USD",
    "x" : "Tisztelettel:",
    "y" : "Gyula"
}

valutak = ['Magyar Forint (HUF)', 'Amerikai Dollár (USD)', 'Angol Font (GBP)', 'Ausztrál Dollár (AUD)', 'Bolgár Leva (BGN)', 'Cseh Korona (CZK)', 'Dán Korona (DKK)', 'Euro (EUR)', 'Horvát Kuna (HRK)', 'Japán Yen (JPY)', 'Kanadai Dollár (CAD)', 'Lengyel Zloty (PLN)', 'Norvég Korona (NOK)', 'Orosz Rubel (RUB)', 'Román Lej (RON)', 'Svájci Frank (CHF)', 'Svéd Korona (SEK)', 'Szerb Dinár (RSD)', 'Török Líra (TRY)']

def valt():

    amount=input("Váltanivaló mennyiség: ")

    valuta_from = ''
    valuta_from=input("Erről a valutáról: ")

    while valuta_from == '':
        for v in valutak:
            print(v)
        valuta_from=input('Erről a valutáról: ')

    valuta_to=input("Erre a valutára: ")

    adat["amount"] = amount
    adat["valuta_from"] = valuta_from
    adat["valuta_to"] = valuta_to

    r = requests.post("https://www.napiarfolyam.hu/arfolyam/valutavalto/", data=adat)

    leves = BeautifulSoup(r.text, 'html.parser')

    try:
        print(amount+' '+valuta_from+' -> '+leves.find('div', {"style":"font-size: 2em; text-align:center; color:#ffffff; height: 200px"}).find('span', {"style":"color: #15AF1C;"}).text)
    except:
        print("Helytelen adatok!")

# kiírja Gyula használatának módját
hasznalat = 'Gyula a következőket tudja:\n\tszótár (sz)\n\tidőjárás (i)\n\tlottó (l)\n\thelyesírás (h)\n\takasztófa (a)\n\tkilépés (k)\n\tmenetrend (m)\n\tdalok tempója (bpm)\n\tvalutaváltó (v)\nA szótárfajták megjelenítéséhez a \'szótárfajták\' (szf) parancsot használjuk!\n'

# kiírja az elérhető szótárfajtákat
szotarak = 'Szótárfajták:\n\t- magyarnemet(mn),\n\t- nemetmagyar(nm),\n\t- magyarangol(ma),\n\t- angolmagyar(am),\n\t- szinonima(az),\n\t- idegen(i)\n'

def main():
	print("Gyula - személyes asszisztens (v0.7.1)")
	
	while True:
	
		parancs = input('>>')
		
		if re.match('id[oő]j[aá]r[aá]s' ,parancs) or parancs == 'i':
		
			hely = input('hol?>>>')
		
			print(elorejelzes(hely))
		
		elif re.match('kil[eé]p[eé]s', parancs) or parancs == 'k':
		
			os.system('clear')
			sys.exit()
			
		elif re.match('lott[oó]', parancs) or parancs == 'l':
		
			print(lotto())
			
		elif re.match('helyes[ií]r[aá]s', parancs) or parancs == 'h':
		
			szo = input('ellenőrizendő>>>')
			
			print(helyese(szo))
			
		elif re.match('sz[oó]t[aá]r', parancs) or parancs == 'sz':
			
			fajta = input('szótárfajta>>>')
			
			szo = input('szó>>>>')
			
			print(szotar(fajta, szo))
		
		elif re.match('sz[oó]t[aá]rfajt[aá]k', parancs) or parancs == 'szf':
		
			print(szotarak)
		
		elif re.match('akaszt[oó]fa', parancs) or parancs == 'a':
		
			akasztofa()
		
		elif parancs == 'menetrend' or parancs == 'm':
		
			menetrend()
		
		
		elif re.match('valutav[aá]lt[oó]', parancs) or parancs == 'v':
			
			valt() 

		elif parancs == 'bpm':

			bpm()

		else:
			print("Ismeretlen parancs!")
			print(hasznalat)
		
if __name__ == "__main__":
	main()


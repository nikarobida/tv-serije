import os
import re
import csv
import Shrani_strani as ss

vzorec_serij = re.compile(
        r'itemprop="ratingValue">(?P<ocena>.*?)</span>.*?'
        r'itemprop="ratingCount">(?P<st_glasov>.*?)</span>.*?'
        r'data-tconst="tt(?P<id>\d{7})".*?'
        r'<h1 itemprop="name" class="">(?P<naslov>.*?)&nbsp;.*?'
        r'datetime=".*?">.*?(?P<dolzina>\d{1,3}\D+)\\n.*?</time>.*?'
        r'>TV .*?Series (?P<leto>\(.*?\)).*?'
        r'"bp_sub_heading">(?P<epizode>\d+) episodes?</span>.*?'
        r'<div class="summary_text" itemprop="description">\\n\s+(?P<opis>.*?)\\n.*?'
        r'<h2>Cast</h2>(?P<igralci>.*?)See full cast.*?'
        r'Genres:</h4>(?P<zanri>.*?)</div>.*?'
        r'Country:</h4>(?P<drzave>.*?)</div>.*?'
        ,flags = re.DOTALL)

def predelaj_podatke(serija):
    seznam_let = re.findall(r'[12][90]\d{2}', serija['leto'])
    k=''
    if len(seznam_let) == 2:
        k = seznam_let[-1]
    serija['leto'] = (seznam_let[0] + '-' + k)
    for x in ['h', 'min']:
        if x in serija['dolzina']:
            h = 1
            if x == 'h':
                h = 60
            cas = h * int(serija['dolzina'].replace(x, ''))
    serija['dolzina'] = cas
    serija['epizode'] = int(serija['epizode'])
    serija['ocena'] = float(serija['ocena'])
    serija['drzave'] = re.findall(r'itemprop=.*?url.*?>(.*?)</a>',
                                  serija['drzave'])
    serija['st_glasov'] = int(serija['st_glasov'].replace(',', ''))
    serija['zanri'] = re.findall(r'stry_gnr"\\n> (\D+?)</a>',
                               serija['zanri'])
    i = re.findall(
        r'itemprop="name">(.*?)</span>.*?<div>.*?&nbsp;(.*?)\\n',
                                   serija['igralci'])
    j = []
    for (x,y) in i:
        y1 = y
        if '<' in y:
            y1=((y.split('>')[1]).split('<')[0])
        j.append((x,y1))
    serija['igralci'] = j
    return serija
    
def zberi_podatke(ime_datoteke):
    '''Zbere podatke o tv seriji iz njene datoteke.'''
    m = ss.trenutna_mapa()
    os.chdir('../imdb')
    with open(ime_datoteke, 'r') as f:
        vsebina = f.read()
    for stvar in re.finditer(vzorec_serij, vsebina):
        serija = stvar.groupdict()
    pr_serija = predelaj_podatke(serija)
    for x in pr_serija:
        print(x, ':', pr_serija[x])
    os.chdir('../' + m)
    
    
    

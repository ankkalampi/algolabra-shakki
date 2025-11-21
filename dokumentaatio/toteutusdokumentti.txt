# Toteutusdokumentti

## Ohjelman yleisrakenne

Toteuttamani shakkisovellus koostuu kolmesta osasta, jotka ovat: 

1) ai-platformin kanssa kommunikointi ja siirtojen lähetys
2) parhaimman siirron laskevan minmax-algoritmin sekä heuristiikkafunktion toteutus
3) varsinainen shakkitoteutus, joka generoi lailliset siirrot jokaiselle pelitilanteelle.

Osa 1 koostuu tiedostosta src/smart_ai.py, osa 2 tiedostoista src/minmax.py ja src/heuristic.py. Loput tiedostot src-kansiossa vastaavat osasta 3.

### Osa 1 - ai-platformin kanssa kommunikointi ja siirtojen lähetys

Tämä osa on käytännössä sama kuin esimerkkiprojektin stupid_ai.py

### Osa 2 - parhaimman siirron laskeva minmax-algoritmi sekä heuristiikkafunktio

Toteutus perustuu alfa-beta -harvennuksella toteutettuun minmax-algoritmiin. Laskennassa käytetään shakkitoteutuksen situation-luokkaa. Situation.py -tiedostoon ollaan toetutettu funktio, jolla situation-olion ja jonkin siirron perusteella voidaan generoida uusi situation-olio, eli pelitilanne johon tämä siirto johtaa, sekä funktio, jolla lailliset siirrot voidaan generoida situation-olion eli pelitilanteen perusteella. Minmax-funktiossa uusia situation-oliota luodaan rekursiivisten funktiokutsujen yhteydessä.

Minmax-algoritmi perustuu parhaimman siirron selvittämiseen laskemalla siirtoketjuja alaspäin sillä periaatteella, että molemmat pelaajat valitsevat aina joka tilanteessa siirron, joka johtaa vuorossa olevan parhaimpaan mahdolliseen asemaan. Joka toisella vuorolla pyritään siis maksimoimaan, ja joka toisella minimoimaan pistemäärä. Siirtoketjut lasketaan syvyyshakuperiaatteella siten, että kun ollaan päästy maksimisyvyyteen, aletaan palauttaa ketjua ylöspäin pistemäärää, johon siirrot johtavat, kun valitaan aina joko maksimi- tai minimipistemäärä riippuen vuorosta. Lopulta ylimmälle tasolle, eli siirtoihin, jotka seuraavat pelitilannetta, josta minmax-algoritmia ollaan alunperin kutsuttu, saadaan jokaista siirtoa kohden tieto siitä, minkä arvoiseen pelitilanteeseen kukin siirto johtaa, kun molemmat pelaajat pelaavat itselleen edullisimmalla tavalla.

Minmax-funktio käyttää pelitilanteiden arvottamiseen melko yksinkertaista heuristiikkafunktiota. Heuristiikka laskee yhteen pelinappuloiden yhteenlasketun arvon (sotilas 1p, lähetti 3p, ratsu 3p, torni 5p, kuningatar 8p). Lisäksi shakituksesta saa kaksi lisäpistettä per shakittava nappula, neljästä keskustaruudusta saa yhden lisäpisteen per nappula, ja vastustajan alueella olemisesta saa yhden lisäpisteen per nappula. Mustan pisteet lasketaan miinuspisteiksi, jolloin negatiivinen pistemäärä tarkoittaa mustan johtoasemaa ja positiivinen pistemäärä puolestaan valkoisen johtoasemaa. 

### Osa 3 - Shakkitoteutus ja laillisten siirtojen generointi

Shakkitoteutuksen ytimessä on bitboardien ja esilaskettujen hyökkäystaulujen käyttö. Bitboard on 64-bittinen kokonaisluku, joka kuvaa shakkilaudan 64 ruutua. Yhdellä bitboardilla voidaan siis kuvata esimerkiksi jonkin nappulatyypin (esim valkoiset ratsut) sijoittumista pelilaudalla. Bitboardissa on siis ykkönen niissä kohdissa, joissa kuvatut nappulat ovat, ja nolla niissä kohdissa joissa ei ole kuvattuja nappuloita. 

Esilasketut hyökkäystaulut sisältävät tiedon eli bitboardin siitä, mihin ruutuihin mikäkin nappula voi mistäkin ruudusta hyökätä tai liikkua. Edeltä käsin laskeminen nopeuttaa siirtomahdollisuuksien selvittämistä merkittävästi, kun pelitilanteen aikana voidaan vain indeksoida taulukkoa ruudun numeron perusteella. Jos halutaan selvittää mihin vaikkapa ratsu voi hyökätä ruudusta 27, se selviää hakemalla bitboard kohdasta knight_attack_table[27].

Lähettien, tornien ja kuningattarien tapaukessa käytetään kaksiulotteisia hyökkäystaulukoita, joissa jokaista ruutua vastaa myös joukko peittoarvoja (block value). Peittoarvo on 12-bittinen luku, joka kuvaa jokaiselle neljälle hyökkäyssuunnalle sitä, monennessako ruudussa tulee vastaan joku toinen nappula. Eli esimerkiksi tornin hyökkäysruudut ruudusta 27 peittoarvon ollessa 000000010001 saadaan selville hakemalla rook_blocking_attack_tables[27][17].

Lailliset siirrot saadaan selville generoimalla ensin hyökkäystaulujen perusteella pseudolailliset siirrot, ja poistamalla sitten ne siirrot, jotka johtavat omien nappuloiden syömiseen tai oman kuninkaan shakkiin. Mikäli tämän poistamisen jälkeen ei ole jäljellä enää yhtäkään siirtoa, ei laillisia siirtoja ole, ja kyseessä on shakkimatti. Tämä voisi tietysti tarkoittaa myös tasapelitilannetta, jossa kuningas ei ole shakissa, mutta laillisia siirtoja ei ole. Tasapeliä ei ole kuitenkaan vielä toteutettu tässä vaiheessa.

## Suorituskyky

Ottaen huomioon, että käytin paljon aikaa bitboardien ja esilaskettujen hyökkäystaulujen toteuttamiseen, suorituskyky on melko lailla pettymys. Tämä järjestelmä kykenee laskemaan pelitilanteita käytännössä vain kolmen siirron syvyyteen siten että siirtojen miettimisajat ovat jotenkin järkeviä. Neljä siirtoakin onnistuu jos siirtoa jaksaa odotella noin minuutin verran, mutta viiden siirron syvyys on jo käytännössä mahdoton saavuttaa järkevässä ajassa.

Itse minmax-algoritmin aikavaativuus on O(b^m), jossa b on keskimääräinen haarautuvuus (eli laillisten siirtojen määrä pelitilanteessa) ja m on syvyys, johon lasketaan. Kun käytännöllinen maksimisyvyys on 3, on tämä siis käytännössä O(b^3). Alfa-beta karsinta parantaa toki tehokkuutta huomattavsti, mutta huonoimman tilanteen aikavaativuus on kuitenkin tämä O(b^3).

Yritin parantaa tehokkuutta järjestämällä siirrot paremmuusjärjestykseen ennen minmaxin kutsumista, mutta tämä hidastikin sovelluksen toimintaa huomattavasti, eikä minulla ollut aikaa selvittää syytä tähän tarkemmin. Minmaxin toimintaa voisi luultavasti tehostaa nykyisestä paljonkin, jos esimerkiksi syyn tähän siirtojen järjestämisen hitauteen selvittäisi. 

## Puutteet ja parannusehdotukset

Kuten mainittua, minmax-algoritmia ei ole alfa-beta -karsintaa lukuun ottamatta juurikaan saatu tehostettua tässä sovelluksessa. On kuitenkin olemassa paljonkin optimointimenetelmiä, jotka perustuvat erityisesti siihen, miten alfa-beta -karsinta saadaan karsimaan mahdollisimman paljon haaroja pois laskennasta. Eräs lupaava menetelmä olisi aloittaa vuoroista, joissa syödään vastustajan nappula, koska nämä useimmin johtavat hyviin asemiin. Omassa toteutuksessani ei varsinaisesti kulje tietoa siitä, syödäänkö nappula vai ei ()  

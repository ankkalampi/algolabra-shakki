### Testausdokumentti

## Testikattavuus

Testikattavuuden selvittäminen on suoritettu käyttäen pytestin pytest-cov -pluginia. Testikattavuusraportti näyttää tältä:

```
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.13.5-final-0 ________________

Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/__init__.py             0      0   100%
src/attack_tables.py       24      0   100%
src/bishop.py              54      0   100%
src/chess_board.py         19     19     0%   1-44
src/globals.py             13      0   100%
src/heuristic.py          177     78    56%   89-92, 95-106, 109-121, 124-132, ...
src/king.py                20      0   100%
src/knight.py              24      0   100%
src/minmax.py              35      1    97%   26
src/pawn.py               172     15    91%   290-293, 353-368
src/precomputation.py     189      0   100%
src/queen.py               29      0   100%
src/rook.py                53      0   100%
src/situation.py          186     31    83%   193-194, 200, 205, 214, 228, 283-317
src/smart_ai.py            66     66     0%   1-128
src/timing.py               2      0   100%
src/utils.py              218    140    36%   12, 39-50, 61-89, 112-136, 172, ...
-----------------------------------------------------
TOTAL                    1281    350    73%
```

Kuten kattavuusraportista käy ilmi, projektia ollaan testattu varsin laajasti. Testaamatta jätetyt chess_board.py ja smart_ai.py ovat hyvin pieniä ja yksinkertaisia, ja liittyvät lähinnä ai-platformin kanssa kommunikointiin. Tästä syystä en ole katsonut tarpeelliseksi testata niitä erikseen. Siirtojen oikeellisuus on kuitenkin testattu muiden tiedsotojen testien yhteydessä. Utils.py:tä ollaan myös testattu varsin vähäisesti. Tämä tiedosto pitää sisällään varsin paljon pieniä ja yksinkertaisia funktioita, joiden oikeellinen toiminta on tullut todistettua esimerkiksi debug-printtausten yhteydessä.


## Mitä on testattu?

Suurin osa testeistä liittyy esilaskettuhin hyökkäystauluihin (precomputed attack tables). Näiden tarkoituksena on laskea etukäteen jokaiselle nappulatyypille jokaista ruutua kohden ne ruudut, joihin kyseinen nappula voi tuosta ruudusta hyökätä. Tornien, lähettien ja kuningattaren tapauksessa on tarpeen laskea vielä jokaista ruutua kohden niin sanotun blokkausarvon perusteella lasketut ruudut, joihin tuosta ruudusta voi hyökätä. Blokkausarvo on 12-bittinen luku, jolla saadaan kätevästi kuvattua, miten kaukana missäkin suunnassa on blokkaava nappula. Näiden taulukoiden laskennan toteuttamisessa oli varsin paljon ongelmia, ja suuri testien määrä heijastelee vaikeahkoa debuggausprosessia.

Esilaskettujen hyökkäystaulujen sekä blokkausarvojen lisäksi on testattu erityisesti siirtojen generoitumista oikein (kaikki lailliset siirrot generoitu, ei laittomia siirtoja), shakin ja shakkimatin oikeellista tarkistamista, sekä sitä, toimiiko parhaimman siirron löytävä minmax-algoritmi oikein. 

Minmax-algoritmia ollaan testattu tilanteessa, jossa shakkimatti on lödettävissä valkoisella kolmen siirron päähän (kun mustan siirto lasketaan mukaan), sekä yhden siirron päähän siten, että peli jatkuu ikään kuin samasta tilanteesta (kunhan musta on tehnyt vuoronsa). Testasin minmax-algoritmia myös viiden siirron päähän, mikä onnistui, mutta olen jättänyt tämän testin pois, koska sen ajamisessa kestää todella pitkään. Mikäli tätä testiä halutaan kokeilla, on test_minmax.py -tiedostossa olemassa tämä testi uloskommentoituna. 

## Minkälaisilla syötteillä testaus tehtiin?

Testisyötteinä ollaan käytetty pelitilannetta kuvaavia Situation-olioita, Yhden pelinappulatyypin sijoittumista kuvaavia 64-bittisiä bitboardeja, siirtoja, jotka ollaan annettu shakkitoteutukseni omalla 18-bittisellä siirtonotaatiolla, sekä tietyissä tapauksissa ruudun numeroa kuvaavana kokonaislukuna. Testien oikeat tulokset ovat niin ikään olleet näitä kaikkia, Situation-olioita lukuunottamatta.

## Miten testit voidaan toistaa?

Ajamalla projektin juuressa:

´´´
pytest
´´´

tai poetryn kautta:

´´´
poetry run pytest tests/
´´´
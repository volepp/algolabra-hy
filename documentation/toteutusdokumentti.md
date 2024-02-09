# Toteutusdokumentti

Ohjelma koostuu ennen kaikkea pelilogiikasta, pelaajaa vastaan pelaavasta tekoälystä ja käyttöliittymästä.

Board-kansiosta löytyy pelilogiikan toteuttava koodi. Tähän kuuluu esimerkiksi laillisten siirtojen etsiminen asemasta ja pelin määrittäminen. Lisäksi moduuli sisältää esimerkiksi liikkumislogiikan jokaiselle eri nappulatyypille (piece-alimoduuli). 

Engine-moduulista puolestaan löytyy pelaajaa vastaan pelaava tekoäly. random.py-tiedostossa oleva implementaatio on testaamista varten ja valitsee joka vuorolla vain satunnaisen siirron. Engine-luokka on varsinainen tekoälytoteutus, joka perustuu minmax-algoritmiin alpha-beta pruningilla tehostettuna. 

Käyttöliittymä on game-moduulissa ja se on toteutettu kolmannen osapuolen kirjastoja (python-chess ja Lichessin Python-kirjasto) käyttäen.

## Aikavaativuus

Minmax on rekursiivinen algoritmi, joka käy läpi kaikki mahdolliset siirtokombinaatiot. Sen aikavaativuus kasvaa täten eksponentiaalisesti suhteessa mahdollisten siirtojen määrään (O(b^d)).

Alpha-beta pruningin avulla pahimmassa tapauksessa aikavaativuus ei muutu minmaxiin verrattuna. Parhaassa tapauksessa alpha-beta pruning voi kuitenkin tiputtaa aikavaativuuden neliöjuureen: O(sqrt(b^d)). 

## Parannusajatukset

Jotta minmax ja alpha-beta pruning voi toimia hyvin, pelilogiikan toteuttavan Board-luokan operaatioiden täytyy toimia nopeasti. Parannusta on tapahtunut, mutta optimoitavaa riittää vielä. Lisäksi peliluokan operaatioiden aika- ja tilavaativuutta voisi tutkia.

## Lähteet

https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
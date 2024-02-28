# Testausdokumentti

CI status: ![CI](https://github.com/volepp/algolabra-shakki/workflows/CI/badge.svg)

Tämänhetkinen testikattavuus: [![codecov](https://codecov.io/gh/volepp/algolabra-shakki/graph/badge.svg?token=R4000SVQ04)](https://codecov.io/gh/volepp/algolabra-shakki)

![Testiraportti](teststatus.png)

## Testien kuvaus

Projektissa testataan ainoastaan pelilogiikaan ja tekoälyyn liittyviä moduuleita eli käytännössä kaikkea `board` ja `engine` moduuleihin sisältyvää. Lichess- ja Ascii-käyttöliittymiä, jotka ovat toteutettu pitkälti kolmannen osapuolen kirjastoja käyttäen, ei siis testata. 

Testit ajetaan CI:ssä automaattisesti ja testeistä generoidaan kattavuusraportti, joka ladataan Codecoviin. Tämän avulla Codecovista saadaan tietoa testikattavuudesta esimerkiksi README:n alkuun ja tähän dokumenttiin.

Tekoälyn testaamiseen on käytetty myös chess.com-sivustolta otettuja puzzle-harjoituksia. Kyseessä on lyhyitä, muutaman siirron sarjoja, jotka johtavat pelaajan voittoon tai voittavaan positioon pääsemiseen. Puzzleista saa hyviä testejä, sillä niihin on objektiivisesti vain yksi oikea vastaus. Tällä hetkellä käytetyt puzzlet ovat erilaisia pakotettuja shakkimatteja kahdella siirrolla. Testi varmistaa, että tekoäly löytää oikean siirron, joka ratkaisee puzzlen.

### Pelilogiikan testaus

Pelilogiikasta testataan Board-, Position- ja eri nappuloiden luokkien avainfunktioita, kuten laillisten siirtojen löytämistä, pelin tuloksen päättelyä, shakkitilanteen tunnistusta ym.. Myös jokaisen nappulan kontrolloitujen ruutujen ja mahdollisten siirtojen laskemista testataan omissa testeissään.

### Tekoälyn testaus

Tekoälyn testaamisessa joitakin merkittäviä funktioita, kuten sort_moves_by_evaluation, testataan erikseen omassa testissään. Varsinaista minmax-algoritmia kuitenkin testataan pääasiassa chess.com-sivustolta haettujen pulmien (puzzles) avulla. Sivulta on kopioitu pulman alkutilanteen FEN-koodi, joka ladataan laudalle (Board-luokasta löytyy funktio pelitilanteen lataamiselle FEN-koodista). Tämän jälkeen varmistetaan, että tekoäly löytää tilanteessa oikean siirron. Jos tavoitteena on löytää tilanteesta pakotettu shakkimatti, varmistetaan tekoälyn palauttaman evaluaation perusteella, että se on nähnyt linjan shakkimattiin asti.

Pulmista tekee hyvän testitapauksen se, että niihin on vain yksi oikea ratkaisu. Muut siirrot ovat yleisesti ottaen paljon huonompia ja joissain tilanteissa voivat jopa johtaa häviävään tilanteeseen. Tekoälyn testaamiseen on kuitenkin tässä vaiheessa valittu vain sellaisia tehtäviä, joissa tietyn siirron valintaperuste on erityisen selkeä (esimerkiksi sen johtaminen pakotettuun shakkimattiin). 

## Testien ajaminen

Testit voi ajaa repositorion juuressa seuraavalla komennolla:

```
pytest src
```

Kattavuusraportin saa ajamalla vastaavasti repositorion juuressa:

```
coverage run --branch -m pytest src; coverage report -m
```
# Viikkoraportti, viikko 4

Toteutin minmax-funktion Engine-luokkaan ja lisäsin siihen alpha-beta pruningin. Lisäksi optimoin Board-luokkaa huomattavasti (ja erotin osan siitä Position-luokkaan), jotta pelipuun läpikäyminen kävisi hieman nopeammin. 

Lisäksi lisäsin testausta Engine-luokalle. Testit tarkistavat, että tekoäly löytää shakkimatin yhdellä tai kahdella siirrolla tilanteissa, jossa tällainen on mahdollista löytää. Otin yhdeksi testicaseksi taktiikkaharjoituksen suoraan chess.comista, joka osoittautui käteväksi tavaksi testata tekoälyä. 

## Tunnit

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 6.2.  | 5h            | Minmax-toteutus ja ab-pruning |
| 8.2.  | 2h            | Pelilogiikan optimoimista |
| 9.2.  | 2h            | Pelilogiikan optimoimista ja Engine-luokan testaamista |
| Yhteensä | 9h         |        |

## Jatko

Pelilogiikkaa pitää vielä optimoida lisää. Samoin sotilaisiin liittyy vielä jonkin verran bugeja, jotka tulee korjata ja joille tulee kehittää testit. Näiden lisäksi position evaluaatioalgoritmia pitää työstää. Tällä hetkellä se toimii erittäin yksinkertaisesti katsomalla molempien puolien materiaalia. 

## Kysymyksiä
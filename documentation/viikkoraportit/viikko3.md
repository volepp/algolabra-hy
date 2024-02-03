# Viikkoraportti, viikko 3

Pelilogiikka on nyt sillä tasolla, että tekoälyn implementoiminen voi alkaa. Muutettiin hieman laillisten siirtojen löytölogiikkaa siten, että nappulat ovat nyt vastuussa sen tietämisestä, mitä ruutuja ne kontrolloivat. Tämän jälkeen board tarkistaa, voiko kontrolloituun ruutuun liikkua. Lisäsin myös testit pelilogiikalle Board-luokassa ja jokaisen nappulan kontrolloitujen ruutujen etsimiselle. En valitettavasti ehtinyt tällä viikolla vielä päässyt työstämään minimax-algoritmia. 

Lisäksi testidokumentin kirjoittaminen aloitettiin.

## Tunnit

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 31.1.  | 2h            | Pelilogiikan toteuttamista |
| 1.2.  | 2h            | Pelilogiikan toteuttamista |
| 3.2.  | 4h            | Pelilogiikan toteuttamista, osittaista refaktorointia ja testaamista |
| Yhteensä | 8h         |        |

## Jatko

Seuraavaksi alan toteuttamaan minimax-algoritmia. Tavoite olisi ensiviikolla päästä siihen tilanteeseen, että minimax-algoritmi toimii, mutta laudan tilanteen evaluointifunktio on kuitenkin vielä alkeellinen (esim. pelkästä materiaalin määrästä laskettu). Pyrin myös toteuttamaan alpha-beta pruningin. Tämä mahdollistaisi sen, että seuraavalla viikolla pääsisi jo keskittymään evaluointialgoritmin parantamiseen.

## Kysymyksiä
# Viikkoraportti, viikko 2

Toisella viikolla lähdin toteuttamaan käyttöliittymiä ja muodostin ohjelman perusrakenteen. Korvasin varsinaisen tekoälyn toistaiseksi ohjelmassa väliaikaisella RandomEngine-luokalla, joka valitsee joka tilanteessa vain satunnaisen siirron. Tässä vaiheessa vielä laillisten siirtojen löytämisessä on huijattu ja käytetty valmiita python-chess-kirjaston työkaluja, mutta varsinaisen pelilogiikan implementointiin aika ei vielä riittänyt. 

Myös testaaminen alustettiin. Toistaiseksi testattavaa ei kovin paljoa ollut, sillä varsinainen pelilogiikkaa on toistaiseksi implementoitu hyvin vähän ja tekoälyn implementoimiseen ei olla päästy lainkaan. Yksikkötestejä kuitenkin lisättiin sille vähälle pelilogiikalle, mitä projektissa on tällä hetkellä toteutettuna.

Lisäksi projektissa siirryttiin käyttämään siirtojen kanssa UCI-formaattia. Vaikka SAN-formaattia näkee käytettävän enemmän kirjoissa ja muualla, kun siirtoja esitetään ihmiselle, on UCI kätevämpi tietokoneiden väliseen kommunikaatioon. UCI-formaatissa siirron notaatio ei ole riippuvainen laudan tilanteesta, joka tekee siitä geneerisemmän ja helpommin käsiteltävän.

## Tunnit

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 25.1.  | 2h            | Käyttöliittymien ja projektirakenteen toteuttaminen |
| 27.1.  | 2h            | Perehtyminen aiheeseen ja määrittelydokumentin kirjoittaminen |
| Yhteensä | 4h         |        |

## Jatko

Seuraavaksi lähden toteuttamaan itse pelilogiikkaa, jonka avulla päästään python-chess-kirjastosta eroon (paitsi ASCII-visualisoinnissa). Toisin sanoin toteutan Board-luokan, joka ylläpitää pelin tämän hetkistä tilaa (nappuloiden paikat jne.). Lisäksi Boardin avulla voidaan hakea laillisia siirtoja, tarkistaa shakit, matit ja patit, yms. 
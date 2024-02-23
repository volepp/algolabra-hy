# Viikkoraportti, viikko 6

Tämä viikko oli pääasiassa minmaxin tehostamista. Implementoin iteratiivisen syvyyshaun siten, että kasvatetaan syvyyttä jokaisella iteraatiolla ja katkaistaan haku, kun syvyyden analysointiin menee yli 5 sekuntia. Lisäksi position evaluointia tehostettiin siten, että siirtoa ei "simuloitu" vaan aiempaa evaluaatiota vain päivitettiin siirron perusteella. 

Lisäksi implementoin yksinkertaisen välimuistin, jota käytetään siihen, että aiemmin parhaaksi todettu siirto positiossa nostetaan uutta syvyyttä analysoidessa ensimmäiseksi läpikäyntijärjestyksessä. Tämä paransi alpha-beta -karsinnan performanssia.

## Tunnit

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 21.2.  | 1h            | Minmaxin tehostamista |
| 22.2.  | 3h            | Minmaxin tehostamista |
| 23.2.  | 2h            | Vertaisarviointi ja dokumentaatioiden päivittäminen |
| Yhteensä | 6h         |        |

## Jatko

Tekoäly tuntuu pelaavan jo ihan hyvällä tasolla. Itse pelaamiseen liittyviä aspekteja voisi parantaa. Esim. laittoman siirron yrittäminen tällä hetkellä kaataa ohjelman ascii-käyttöliittymällä. Tällaisten fiksaaminen pitäisi olla suoraviivaista. Lisäksi voisin tarkistaa, että Lichess-integraatio toimii vielä. Tämä olisi demossa mukava. Näiden jälkeen voisin vielä koittaa parantaa minmaxin tehokkuutta tai evaluointialgoritmia mahdollisuuksien mukaan. 

## Kysymyksiä
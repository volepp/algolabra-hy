# Viikkoraportti, viikko 4

Tällä viikolla keskityin korjaamaan joitakin havaitsemiani bugeja ja parantelemaan pelitilanteen evaluointialgoritmia. Sain ohjelman pelaamaan jo huomattavasti järkevämmin. Yksi merkittävä parannus on se, että keskustan kontrolloimiselle annetaan nyt enemmän painoarvoa. Tämä antoi ohjelmalle jonkinlaisen suunnan siirtojen miettimiseen tilanteessa, jossa välitöntä materiaalin menettämis- tai saantimahdollisuutta ei ole. Lopputulos oli jo paljon luonnollisemmalta tuntuva vastustaja, mutta parannettavaa ehdottomasti vielä on. 

Lisäksi kävin läpi vetaispalautteessa toisen opiskelijan projektin, joka antoi joitakin ideoita omankin projektin parantamiseen.

## Tunnit

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 14.2.  | 1h            | Pelilogiikan korjaamista |
| 15.2.  | 3h            | Evaluointialgoritmin parantamista, bugifiksailua |
| 17.2.  | 3h            | Vertaisarviointi ja dokumentaatioiden päivittäminen |
| Yhteensä | 7h         |        |

## Jatko

Evaluointialgoritmin jatkokehityksen lisäksi tässä kohtaa olisi hyvä saada itse minmax-algoritmia siten kehitettyä, että läpikäytävien positioiden määrä minimoitaisiin. Koen, että Board-luokka toimii tässä kohtaa riittävän nopeasti ja paras tapa tehostaa parhaan siirron hakemista ja lisätä syvyyttä on juurikin huonojen siirtokandidaattien nopea eliminointi. 

## Kysymyksiä
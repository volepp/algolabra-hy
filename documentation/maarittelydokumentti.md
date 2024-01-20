# Määrittelydokumentti

Projekti on tehty osana Helsingin Yliopiston kurssia Aineopintojen harjoitustyö: Algoritmit ja tekoäly, periodi 3, kevät 2024.

Opinto-ohjelma: Tietojenkäsittelytiede, kandidaatin tutkinto

Projektissa toteutetaan shakkipeli ja ihmistä vastaan pelaava tekoälyohjelma.

## Projektin kuvaus

Itse pelin toteutuksessa ajatuksena on, että peliä voi pelata joko komentoriviltä tekstisyötteen avulla, tai Lichessissä bottia vastaan. Tekstimuotoisessa pelissä käyttäjä syöttää tekemänsä siirrot [SAN-formaatissa](https://www.chessprogramming.org/Algebraic_Chess_Notation#Standard_Algebraic_Notation_.28SAN.29). Jälkimmäinen vaihtoehto vaatii, että käyttäjällä on Lichessissä bottitunnus ja tälle käyttäjälle bottipelien pelaamisen oikeuttava API token. Komentorivillä pelatessa lauta voidaan esittää pelaajalle ASCII-muodossa. Ulkoisia kirjastoja tullaan käyttämään käyttöliittymää varten, ennen kaikkea [Lichessin Python-kirjastoa](https://github.com/lichess-org/berserk) ja [python-chess-kirjastoa](https://python-chess.readthedocs.io/en/latest/). Pelin tilan ylläpitämiseen ei tulla käyttämään valmista kirjastoa, vaan nappuloiden paikat tallennetaan 8x8 taulukkoon omina objekteinaan. Pelitilan sisältävä luokka pystyy täten esimerkiksi kertomaan laillisista siirroista, pelin päättymisestä tasapelin tai shakkimatin yhteydessä, ja tarvittaessa palauttamaan laudan tilanteen [FEN-muotoisena](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation) merkkijonona.

Pelaajaa vastaan pelaava tekoäly taas perustuu minimax-algoritmiin, jota tehostetaan alpha-beta-karsinnalla. Algoritmi lähtee laskemaan siirtoja eteenpäin nykytilanteesta ja evaluoi jokaisen siirron jälkeen laudan tilanteelle heuristisesti numeerisen arvon. Positiivinen arvo tarkoittaa, että etu on valkeilla, kun taas negatiivinen arvo tarkoittaa mustan etua. Luvun itseisarvon suuruus kertoo edun merkittävyydestä. Täten minimax-algoritmilla pyritään siis etsimään pelipuusta siirto, joka käytössä olevalla laskentasyvyydellä tuottaa tietokoneelle mahdollisimman edullisen tilanteen. Oletuksena on, että kumpikin pelaaja tekee jokaisessa tilanteessa parhaan mahdollisen siirron. Koska tutkittavien variaatioiden määrä kasvaa eksponentiaalisesti laskentasyvyyden funktiona, alpha-beta-karsintaa käytetään eliminoimaan huonolta vaikuttavat polut mahdollisimman nopeasti algoritmin toiminnan tehostamiseksi.

## Ohjelmointikielet ja työkalut

Toteutuksen ohjelmointikielenä on Python ja koodissa käytettävä kieli tulee olemaan englanti. Tämä koskee myös koodissa olevia kommentteja. 

Riippuvuuksien hallintaan tullaan käyttämään [Poetrya](https://python-poetry.org/) ja testaamisessa tavoite on kattava yksikkötestaus [Unittest-sovelluskehystä](https://docs.python.org/3/library/unittest.html) käyttäen.

Pythonin lisäksi vertaispalautetta voin antaa myös ainakin Javalla ja Go:lla tehdyille projekteille. Tarpeen vaatiessa myös JavaScript- ja C++-projektien arvioiminen on mahdollista.

## Dokumentaatio

Kaikki projektiin liittyvä dokumentaatio tullaan kirjoittamaan suomeksi. Myös englanninkielisten projektien vertaisarvoiminen onnistuu.

## Lähteet

https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
https://en.wikipedia.org/wiki/Game_tree
https://www.chessprogramming.org/Algebraic_Chess_Notation#Standard_Algebraic_Notation_.28SAN.29s
https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

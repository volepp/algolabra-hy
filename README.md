# Algolabra - Shakki

[![codecov](https://codecov.io/gh/volepp/algolabra-shakki/graph/badge.svg?token=R4000SVQ04)](https://codecov.io/gh/volepp/algolabra-shakki)
![CI](https://github.com/volepp/algolabra-shakki/workflows/CI/badge.svg)

Helsingin Yliopiston kurssia *Aineopintojen harjoitustyö: Algoritmit ja tekoäly* varten tehty shakkipeli ja ihmistä vastaan pelaava tekoälyohjelma.

## Dokumentaatio

[Määrittelydokumentti](documentation/maarittelydokumentti.md)

## Viikkoraportit

[Viikko 1](documentation/viikkoraportit/viikko1.md)

[Viikko 2](documentation/viikkoraportit/viikko2.md)

# Pelaaminen

Ohjelmaa vastaan voi pelata joko komentorivillä ASCII-käyttöliittymää käyttäen tai Lichessissä yhdistämällä ohjelman bottikäyttäjään, jonka siirrot se tekee. 

## Pelaaminen komentorivillä

Pelataksesi komentorivillä, aja ohjelma ilman argumentteja:

```
python3 src/main.py
```

## Pelaaminen Lichessissä

Voit pelata ohjelmaa vastaan Lichessissä antamalla sille access tokenin bottikäyttäjälle. Ohjeita tokenin hankkimiseen löytyy [täältä](https://github.com/lichess-bot-devs/lichess-bot/wiki/How-to-create-a-Lichess-OAuth-token).

Kun token on hankittu, sen voi antaa ohjelmalle kolmella tavalla:

1. Määrittelemällä ympäristömuuttujan `LICHESS_TOKEN=<token>`
1. Luomalla secret/.env tiedoston ja lisäämällä sinne rivin `LICHESS_TOKEN=<token>`.
1. komentoriviargumenttina `--token <token>`.

Käynnistääksesi ohjelma Lichess-moodissa, lisää komentoon `--lichess` (ja halutessasi `--token`) flagi:

```
python3 src/main.py --lichess (--token <token>)
```

Kun ohjelma on käynnissä, lähetä bottikäyttäjälle haaste aloittaaksesi pelin.
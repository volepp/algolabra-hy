# Testausdokumentti

CI status: ![CI](https://github.com/volepp/algolabra-shakki/workflows/CI/badge.svg)

Tämänhetkinen testikattavuus: [![codecov](https://codecov.io/gh/volepp/algolabra-shakki/graph/badge.svg?token=R4000SVQ04)](https://codecov.io/gh/volepp/algolabra-shakki)

![Testiraportti](teststatus.png)

## Testien kuvaus

Projektissa testataan ainoastaan pelilogiikaan ja tekoälyyn liittyviä moduuleita eli käytännössä kaikkea `board` ja `engine` moduuleihin sisältyvää. Lichess- ja Ascii-käyttöliittymiä, jotka ovat toteutettu pitkälti kolmannen osapuolen kirjastoja käyttäen, ei siis testata. 

Testit ajetaan CI:ssä automaattisesti ja testeistä generoidaan kattavuusraportti, joka ladataan Codecoviin. Tämän avulla Codecovista saadaan tietoa testikattavuudesta esimerkiksi README:n alkuun ja tähän dokumenttiin.

## Testien ajaminen

Testit voi ajaa repositorion juuressa seuraavalla komennolla:

```
pytest src
```

Kattavuusraportin saa ajamalla vastaavasti repositorion juuressa:

```
coverage run --branch -m pytest src; coverage report -m
```
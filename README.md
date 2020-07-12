# Discord-bot-Ture Björkman

En bot till kvasiföreningen Köpstopps egna Discord.


## Hur du använder den

| Kommando | Utförande |
|----------|-----------|
| !boken   | Ture frågar efter boken |


## Todo

* ~~Lägga till botten till servern~~
* ~~Kryptera OAuth nyckeln till botten så den inte ligger publikt på github~~
* CI/CD med Jenkins
* Installera den på raspberry pi
* Skapa fler kommandon
* Skapa en lokal och en "live" version av Ture

## Installera

Installera senaste python och pip.

```
pip install discord.py

# Shitdows
py -3 -m pip install -U discord.py
```

## Hur du startar Ture
Just nu finns det bara en lokal version av ture, men så fort den rullar på Raspberryn så kommer det finnas två eller flera.
För att starta Ture skriver du följande:

` python bot.py 01 xxx `

Där 01 betyder att det är bot#1, 02 är bot#2 osv. _xxx_ är lösenordet till Ture för att avkryptera nycklarna.



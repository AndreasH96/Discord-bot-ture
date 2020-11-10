# Discord-bot-Ture Björkman

En bot till kvasiföreningen Köpstopps egna Discord.


## Hur du använder den

| Kommando | Utförande |
|----------|-----------|
| !help	   | Ture retunerar alla kommandon han kan. |
| !boken   | Ture frågar efter boken. |
| !drinking_game | Ture berättar reglerna för Skrotnisse Drinking-game. |
| !skrotnisse x | Ture skickar länken till det avsnitt av Skrotnisse du ber om. |
| !snapsvisa | Ture ger dig en slumpvald snapsvisa, skål! |
| !askTure | Ställ en valfri fråga till Ture |
| | Följande är admin kommandon. |
| !pi [temp, load, disk, all] | Retunerar respektive status. |
| !info_message_food | Skriver reglerna i matkanalen |
| !info_message_kopstopp | Skriver välkomstmeddelandet i Köpstopp kanalen |


## Buggar och nya Features
För att rapportera en bugg eller om du vill komma med förslag på en ny feature så skapa en issue och tagga den.


## Installera

Installera senaste python och pip. Rekommenderar att köra python i en virtual environment, isf döp mappen där din venv ligger i till `env`. Alternativt att du lägger till namnet på mappen i `.gitignore`.

```
pip install -r requirements.txt

# Shitdows
py -3 -m pip install -U discord.py
```

## Hur du startar Ture
För att starta Ture lokalt skriver du följande:

` python bot.py 01 xxx `

Där 01 betyder att det är bot#1, 02 är bot#2 osv. _xxx_ är lösenordet till Ture för att avkryptera nycklarna. Just nu finns bara 01.



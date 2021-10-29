# Pokemon API

This repository contains a Django Framework site developed to provide a Database acces by means of `GET`-`JSON` based API.

By running this Djiango site you will be able to:

1. Load the `Data/pokemon.json` by means of a web interface which populates the internal DB.
2. Access the API interface as a client `client/client.py`

## Installation

1. Create the necessary virtualenv and activate it:

```cmd
> python -m venv .\venv
> .\venv\Script\activate
> python -m pip install -r requirements
```
2. Django Framework requires a DB initialization:

```cmd
> .\server\clean_db.bat
```
The same script can be used to reset the DB.

3. Start the server:
```cmd
> .\server\run.bat
```
Default configuration allow the access at `http://127.0.0.1:8000`

4. By accessing `http://127.0.0.1:8000` you will be prompted with the choice of a file to upload. Please choose `Data/pokemon.json` and click `Load`.

5. A sample code can be run as:
```cmd
> python client\client.py
```

## Testing and environment
The code has been developed using:
- Python 3.9
- Django 3.2
- Windows 10

A basic test based on Django testing framework can be run with:
```cmd
> python server\pkmnsite\manage.py test pkmnapi
```

## Implemented features
- Model implementation of the `pokemon.json` entry: `class PkmnModel` in `server\pkmnsite\pkmnapi\models.py`
- Parsing of `pokemon.json` and application of requested conditions/exclusion: `server\pkmnsite\pkmnapi\pkmn.py`
- Implementation of API endpoint at `/pokemon` inside `server\pkmnsite\pkmnapi\views.py`
  - `\pokemon?name=Oddish` match name query.
  - `\pokemon?search=odish` Levenshtein name search.
  - `\pokemon?hp=100` field matching.
  - `\pokemon?hp[lt]=100` query options.
  - `\pokemon?type=Grass` by Type 1/2.
  - `\pokemon?hp[gte]=100&defense[lte]=200` concatenation.
  - `\pokemon?&page=1` paging.
- Basic testing by Django Testing Framework: `server\pkmnsite\pkmnapi\tests.py`
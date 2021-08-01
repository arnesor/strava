# Strava
This repo shows how to get your Strava activities and contains examples of how to analyse
the activities. It is based on the article
[Using Python to Connect to Strava’s API and Analyse Your Activities — Dummies Guide](https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86).

## Initial setup
After cloning the repo, go to the cloned directory and run the following commands to install
the necessary packages in a virtual environment. If you don't have pipenv installed, install
it first as described on https://pypi.org/project/pipenv/ and add it to the path.

```bash
pipenv shell
pipenv install
```

As a first time setup you need to replace the values for `client_id`, `client_secret` and
`client_id` in the source code (line 9-11) with values for your Strava account. The article
above describes how to find these values.

## Usage
```bash
python main.py
```

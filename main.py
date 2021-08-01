import json
import time
from pathlib import Path

import pandas as pd
import requests

# Replace the values below with the values for your Strava account
client_id = [INSERT_CLIENT_ID_HERE]
client_secret = '[INSERT_CLIENT_SECRET_KEY]'
code = '[INSERT_CODE_FROM_URL_HERE]'


def get_initial_tokens(file):
    # Make Strava auth API call with your client_code, client_secret and code
    print(f'Token file {file} not found. Requesting initial tokens...')
    response = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )
    # Save json response as a variable
    strava_tokens = response.json()
    print('Received tokens:')
    print(strava_tokens)
    # Save tokens to file
    with open(file, 'w') as outfile:
        json.dump(strava_tokens, outfile)
    print('Getting tokens completed.')
    return strava_tokens


def get_updated_tokens(file):
    # Get the Strava tokens from file
    print(f'Token file {file} found. Reading tokens from file...')
    with open(file) as json_file:
        strava_tokens = json.load(json_file)
    # If access_token has expired then use the refresh_token to get a new access_token
    if strava_tokens['expires_at'] < time.time():
        print('Access_token expired. Getting new access_token...')
        # Make Strava auth API call with current refresh token
        response = requests.post(
            url='https://www.strava.com/oauth/token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': strava_tokens['refresh_token']
            }
        )
        new_strava_tokens = response.json()
        # Save new tokens to file and use the new tokens
        with open(file, 'w') as outfile:
            json.dump(new_strava_tokens, outfile)
        print('Getting tokens completed.')
        return new_strava_tokens
    else:
        print('Getting tokens completed.')
        return strava_tokens


def get_all_fields(access_token):
    # Loop through all activities
    page = 1
    url = "https://www.strava.com/api/v3/activities"
    json_responses = []
    while True:
        # get pages of activities from Strava
        print(f'Getting page {page}...')
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()
        # if no results then exit loop
        if not r:
            break
        json_responses.extend(r)
        page += 1

    df = pd.json_normalize(json_responses)
    df.to_csv('strava_activities_all_fields.csv')


def get_custom_fields(access_token):
    # Loop through all activities
    page = 1
    url = "https://www.strava.com/api/v3/activities"
    # Create the dataframe ready for the API call to store your activity data
    activities = pd.DataFrame(
        columns=[
            "id",
            "name",
            "start_date_local",
            "type",
            "distance",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain",
            "end_latlng",
            "external_id",
        ]
    )
    while True:
        # get page of activities from Strava
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()
        # if no results then exit loop
        if not r:
            break

        # otherwise add new data to dataframe
        for x in range(len(r)):
            activities.loc[x + (page - 1) * 200, 'id'] = r[x]['id']
            activities.loc[x + (page - 1) * 200, 'name'] = r[x]['name']
            activities.loc[x + (page - 1) * 200, 'start_date_local'] = r[x]['start_date_local']
            activities.loc[x + (page - 1) * 200, 'type'] = r[x]['type']
            activities.loc[x + (page - 1) * 200, 'distance'] = r[x]['distance']
            activities.loc[x + (page - 1) * 200, 'moving_time'] = r[x]['moving_time']
            activities.loc[x + (page - 1) * 200, 'elapsed_time'] = r[x]['elapsed_time']
            activities.loc[x + (page - 1) * 200, 'total_elevation_gain'] = r[x]['total_elevation_gain']
            activities.loc[x + (page - 1) * 200, 'end_latlng'] = r[x]['end_latlng']
            activities.loc[x + (page - 1) * 200, 'external_id'] = r[x]['external_id']
        # increment page
        page += 1
    activities.to_csv('strava_activities.csv')


def main():
    tokens_file = Path('strava_tokens.json')
    if not tokens_file.exists():
        strava_tokens = get_initial_tokens(tokens_file)
    else:
        strava_tokens = get_updated_tokens(tokens_file)

    get_all_fields(strava_tokens['access_token'])
    get_custom_fields(strava_tokens['access_token'])


if __name__ == '__main__':
    main()

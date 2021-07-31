import pandas as pd
import requests
import json
import time


def get_all_fields():
    # Get the tokens from file to connect to Strava
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    # Loop through all activities
    url = "https://www.strava.com/api/v3/activities"
    access_token = strava_tokens['access_token']
    # Get first page of activities from Strava with all fields
    res = requests.get(url + '?access_token=' + access_token)
    res = res.json()

    df = pd.json_normalize(res)
    df.to_csv('strava_activities_all_fields.csv')


def get_initial_tokens():
    # Make Strava auth API call with your client_code, client_secret and code
    response = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': [INSERT_CLIENT_ID_HERE],
            'client_secret': '[INSERT_CLIENT_SECRET_KEY]',
            'code': '[INSERT_CODE_FROM_URL_HERE]',
            'grant_type': 'authorization_code'
        }
    )
    # Save json response as a variable
    strava_tokens = response.json()
    # Save tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)
    # Open JSON file and print the file contents
    # to check it's worked properly
    with open('strava_tokens.json') as check:
        data = json.load(check)
    print(data)


def main():
    # Get the tokens from file to connect to Strava
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    # If access_token has expired then use the refresh_token to get the new access_token
    if strava_tokens['expires_at'] < time.time():
        # Make Strava auth API call with current refresh token
        response = requests.post(
            url='https://www.strava.com/oauth/token',
            data={
                'client_id': 56276,
                'client_secret': 'b7f83cba1cbb8bbd44eebe5d7e95d99f6582004a',
                'grant_type': 'refresh_token',
                'refresh_token': strava_tokens['refresh_token']
            }
        )
        # Save response as json in new variable
        new_strava_tokens = response.json()
        # Save new tokens to file
        with open('strava_tokens.json', 'w') as outfile:
            json.dump(new_strava_tokens, outfile)
        # Use new Strava tokens from now
        strava_tokens = new_strava_tokens
    # Loop through all activities
    page = 1
    url = "https://www.strava.com/api/v3/activities"
    access_token = strava_tokens['access_token']
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
            "external_id"
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


if __name__ == '__main__':
    # get_initial_tokens()
    # get_all_fields()
    main()

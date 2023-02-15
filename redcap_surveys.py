import pandas as pd
import requests
import datetime

def get_timing(record, token):
    while True:
        # record = input("Enter record # (e to exit): ")
        # if record == 'e':
        #     exit()

        data = {
            'token': token,
            'content': 'record',
            'action': 'export',
            'format': 'json',
            'type': 'flat',
            'csvDelimiter': '',
            'records[0]': record,
            'events[0]': 'selfreport_measure_arm_1',
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'exportSurveyFields': 'true',
            'exportDataAccessGroups': 'false',
            'returnFormat': 'json'
        }

        try:
            r = requests.post('https://redcap01.brisc.utah.edu/ccts/redcap/api/',data=data)
            #print('HTTP Status: ' + str(r.status_code))
            results = r.json()[0]
            break
        except:
            print("Record ID not valid")
            record = input("Enter consented record ID: ")

    search_complete = 'complete'
    search_timestamp = 'timestamp'

    survey_data = [{'name': 'consent'},
                    {'name': 'demographics'},
                    {'name': 'aamas'},
                    {'name': 'derssf'},
                    {'name': 'ctq'},
                    {'name': 'geqa'},
                    {'name': 'avi'},
                    {'name': 'neopi'}]

    for key, value in results.items():
        if key.endswith(search_complete) or key.endswith(search_timestamp):
            for entry in survey_data:
                if key.split('_')[0] == entry['name']:
                    if key.endswith(search_complete):
                        entry['complete'] = "yes" if value == '2' else "no"
                    elif key.endswith(search_timestamp):
                        entry['timestamp'] = value

    survey_df = pd.DataFrame(survey_data)
    survey_df['timestamp'] = pd.to_datetime(survey_df['timestamp'])

    #print(np.isnat(survey_df['timestamp'][2]))

    # print(type(survey_df['timestamp'][2]))
    # print(isinstance(survey_df['timestamp'][2], pd._libs.tslibs.nattype.NaTType))


    duration = []
    for i, row in survey_df.iterrows():
        #print(row['timestamp'])
        if i == 0:
            duration.append(0)
        elif isinstance(survey_df.loc[i-1, 'timestamp'], pd._libs.tslibs.nattype.NaTType) and i >= 2:
            duration.append(survey_df.loc[i, 'timestamp']-survey_df.loc[i-2, 'timestamp'])
        else:
            duration.append(survey_df.loc[i, 'timestamp']-survey_df.loc[i-1, 'timestamp'])

    survey_df['duration'] = duration

    print(f"REDCap Surveys for {record}")
    print(survey_df)

    total_duration = datetime.timedelta()
    for i, row in survey_df.iterrows():
        if type(row['duration']) != int and \
        not isinstance(row['duration'], pd._libs.tslibs.nattype.NaTType):
            total_duration += row['duration']
    print(f"Total duration: {total_duration}\n")

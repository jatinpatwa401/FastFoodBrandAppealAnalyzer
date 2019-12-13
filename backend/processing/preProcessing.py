import re
import csv
import json
import urllib3
import urllib3.request
from datetime import datetime

# Get list of state names mapped from their name to abbreviation
stateNames = {
    'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE',
    'District of Columbia': 'DC','Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS',
    'Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS',
    'Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY',
    'North Carolina': 'NC','North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Palau': 'PW',
    'Pennsylvania': 'PA','Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT',
    'Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY',
}
# Get list of state names mapped from their abbreviation to name
stateCodes = dict(map(reversed, stateNames.items()))

http = urllib3.PoolManager()

rawData = open('../data/csvFiles/labeledData.csv', 'r')
cleanData = open('../data/processedLocation.csv','w')

data = csv.reader(rawData, delimiter=',')
writer = csv.writer(cleanData, delimiter=',', quoting=csv.QUOTE_MINIMAL)

for row in data:
    stateName = ''
    stateCode = ''
    countryName = ''
    countryCode = ''
    # Set to unknown if location null
    if(row[11] == '' or row[11] == 'unknown'):
        if(row[11] == ''):
            row[11] = 'unknown'
    else:
        userLoc = row[11]
        try: # Call API to get states and countries from user location
            userLoc = re.sub(r'[^a-zA-Z ]+', '', userLoc)
            url = "http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false&address=" + userLoc
            response = http.request('GET', url)
            info = json.loads(response.data.decode('utf-8'))
            # Valid location
            if info.get('status') != 'ZERO_RESULTS':
                try:
                    print(datetime.now())
                    for field in info.get('results')[0].get('address_components'):
                        for Type in field.get('types'):
                            # Found state-level information
                            if(Type == 'administrative_area_level_1'):
                                st = field.get('short_name')
                                if stateNames.get(st):
                                    stateName = st
                                    stateCode = stateNames.get(st)
                                elif stateCodes.get(st):
                                    stateName = stateCodes.get(st)
                                    stateCode = st
                            # Found country-level information
                            if(Type == 'country'):
                                countryName = field.get('long_name')
                                countryCode = field.get('short_name')
                except:
                    print("Error: Failed to get location")
            # User location is invalid. Set to unknown
            else:
                row[11] = 'unknown'
        except:
            print("Error: Failed to call API")
    # Update values if found. Leave blank if not found.
    row.append(stateName)
    row.append(stateCode)
    row.append(countryName)
    row.append(countryCode)
    # Write to cleaned data file
    writer.writerow(row)

rawData.close()
cleanData.close()
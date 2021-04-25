import csv, os, requests
from collections import Counter
from progress.bar import Bar

os.system('clear')

csv_data_filename = 'location_data.csv'

API_KEY = 'PUT YOUR POSITIONSTACK REVERSE GEOCODING API KEY HERE'


locations = []

line_count = len(open(csv_data_filename).readlines(  ))
bar = Bar('Processing location data  ', max=line_count)

with open(csv_data_filename) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		try:
			location = requests.get(f'http://api.positionstack.com/v1/reverse?access_key={API_KEY}&query={row[3]},{row[4]}').json()
			location = location['data'][0]['name']
			os.system('clear')
			bar.next()
			print('\n')
			print(f'Found location near {row[3]},{row[4]} : {location}')

			locations.append(location)
		except:
			pass
bar.finish()

results = [item for items, c in Counter(locations).most_common()
                                      for item in [items] * c]
locations.clear()
for location in results:
	locations.append(f'{location},{results.count(location)}')
results = [i for n, i in enumerate(locations) if i not in locations[:n]]

os.system('clear')

print('Locations in dataset, sorted by frequency:\n\n')
for location in results:
	if (location.split(",")[-1]) == '1':
		print(f'{(location.split(",")[0])}: in dataset {(location.split(",")[-1])} time\n')
	else:
		print(f'{(location.split(",")[0])}: in dataset {(location.split(",")[-1])} times\n')

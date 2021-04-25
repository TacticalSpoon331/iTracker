import csv, os, requests
from collections import Counter
from progress.bar import Bar

os.system('clear')

csv_data_filename = 'location_data.csv'
data_collection_frequency = 300

API_KEY = ''

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
	instance_count = int(location.split(",")[-1])

	time = instance_count * data_collection_frequency

	day = time // (24 * 3600)
	time = time % (24 * 3600)
	hour = time // 3600
	time %= 3600
	minute = time // 60
	time %= 60
	second = time

	if day == 0 and hour == 0 and minute < 45:
		pass
	else:
		print(f'{(location.split(",")[0])}: in dataset {instance_count} times ({int(day)} days, {int(hour)} hours, {int(minute)} minutes, and {int(second)} seconds)\n')

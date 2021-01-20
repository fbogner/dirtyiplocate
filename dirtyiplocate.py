import csv
import argparse
import sys

parser = argparse.ArgumentParser(description='A small script for quick and dirty bulk IP geolocation')
parser.add_argument('--ips',metavar='ips.txt',required=True, help='A text file containing one IP per line to geolocate.')
parser.add_argument('--output',metavar='location.csv',required=True, help='The output csv file containing the IP location data. Existing data will be overwritten.')
parser.add_argument('--append', action='store_true',help='Append to the output file instead of overwriting')

args = parser.parse_args()


# try to import the geo location API 
# ======================================================
try: 
	import geoip2.database
except ImportError:
	print('It looks like you have not installed geoip2')
	print('Please run: pip install geoip2')
	print()
	print('For more information visit: https://pypi.org/project/geoip2/')
	sys.exit(1)


# open geolocation database
# ======================================================
city_db='GeoLite2-City.mmdb'

try: 
	reader = geoip2.database.Reader('./'+city_db)
except FileNotFoundError:
	print('Geo location Database not found: GeoLite2-City.mmdb')
	print()
	print('To get it, do the following:')
	print('1.) Register here: https://www.maxmind.com/en/geolite2/signup')
	print('2.) Access your account here: https://www.maxmind.com/en/account/login')
	print('3.) Select "Download Files" from the left menu')
	print('4.) Download "GeoLite2 City" as .mmdb file (not the CSV)')
	print('5.) Save it along this script as GeoLite2-City.mmdb')
	sys.exit(2)


# Check if we append or overwrite
# ======================================================
mode='w'

if (args.append):
	mode='a'


# Do the actual work
# ======================================================
# open the destination file in append mode
count=0

with open(args.output, mode, newline='') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	# Add header row
	if (not args.append):
		spamwriter.writerow([
			'IP',
        	'Country Code',
    		'Country name',
        	'Postal Code',
			'Most Specific Name',
			'City Name',
			'Latitude',
			'Longitude'
		])
	
	# open the source ip file
	with open(args.ips) as ipfile:
		# for each IP ...
		for ip in ipfile:
			# ... do the geolocation magic ...
			try:
				response = reader.city(ip.strip())
				count=count+1
				
				# and save the result to the CSV
				spamwriter.writerow([
					ip.strip(),
        			response.country.iso_code,
        			response.country.name,
        			response.postal.code,
					response.subdivisions.most_specific.name,
					response.city.name,
					response.location.latitude,
					response.location.longitude
				])
			except geoip2.errors.AddressNotFoundError:
				print("IP "+ip.strip()+" not found")

print(str(count)+" IPs have been geolocated.")
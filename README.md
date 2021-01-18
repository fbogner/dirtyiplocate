# dirtyiplocate
A small script for quick and dirty bulk IP geolocation
Built on top of GeoLite2 (https://pypi.org/project/geoip2/)

* Input: List of IPs
* Output: CSV file with geolocation data for each input IP

# Usage
dirtyiplocate.py [-h] --ips ips.txt --output location.csv [--append] 

optional arguments:
  -h, --help            show this help message and exit
  --ips ips.txt         A text file containing one IP per line to geolocate.
  --output location.csv
                        The output csv file containing the IP location data. Existing data will be overwritten.
  --append              Append to the output file instead of overwriting

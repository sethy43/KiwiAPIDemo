import requests
import json
import urllib.request
import sys
from datetime import datetime, date, timedelta

startRange = datetime.today() + timedelta(days=1)
endRange = datetime.today() + timedelta(days=365)
#print(startRange.strftime("%d/%m/%Y"))
#print(endRange.strftime("%d/%m/%Y"))

destparams = {
	"fly_from": 'airport:MAN',
    "one_for_city" : 1,
    "date_from" : '%s' % (startRange.strftime("%d/%m/%Y")),
    "date_to" : '%s' % (endRange.strftime("%d/%m/%Y")),
    "limit" : 200,
    "sort" : 'price',
    "curr" : 'GBP',
    "max_stopovers" : 0 ,
    "partner" : 'picky'
}


parameters = {
    "fly_from": 'airport:MAN',
    #"fly_to": 'airport:DUB',
    #"one_for_city" : 1,
    "date_from" : '%s' % (startRange.strftime("%d/%m/%Y")),
    "date_to" : '%s' % (endRange.strftime("%d/%m/%Y")),
    "dtime_from" : '17:00',
    "dtime_to" : '20:00',
    "ret_dtime_from" : '09:00',
    "ret_dtime_to" : '17:00',
    "limit" : 1,
    "sort" : 'price',
    "curr" : 'GBP',
    #"currency_rate" : 0.84,
    #"lang" : 'en',
    "flight_type" : 'round',
    "fly_days" : [5],
    "ret_fly_days" : [0,1],
    "nights_in_dst_from" : 2,
    "nights_in_dst_to" : 3,
    "max_stopovers" : 0 ,
    #"stopover_to" : '03:00',
    "partner" : 'picky'
}

familyparameters = {
    "fly_from": 'airport:MAN',
    #"fly_to": 'airport:DUB',
    #"one_for_city" : 1,
    "date_from" : '%s' % (startRange.strftime("%d/%m/%Y")),
    "date_to" : '%s' % (endRange.strftime("%d/%m/%Y")),
    "adults" : 2,
    "children" : 1,
    "dtime_from" : '17:00',
    "dtime_to" : '20:00',
    "ret_dtime_from" : '09:00',
    "ret_dtime_to" : '17:00',
    "limit" : 1,
    "sort" : 'price',
    "curr" : 'GBP',
    #"currency_rate" : 0.84,
    #"lang" : 'en',
    "flight_type" : 'round',
    "fly_days" : [5],
    "ret_fly_days" : [0,1],
    "nights_in_dst_from" : 2,
    "nights_in_dst_to" : 3,
    "max_stopovers" : 0 ,
    #"stopover_to" : '03:00',
    "partner" : 'picky'
}

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def Sort(sub_li): 
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    sub_li.sort(key = lambda x: x[0]) 
    return sub_li 



response = requests.get("https://api.skypicker.com/flights", params=destparams)
destinations = response.json()['data']
varss = []

for airport in destinations:
	parameters.update({"fly_to" : "airport:%s" % (airport['cityCodeTo'])})
	#print(parameters)
	response2 = requests.get("https://api.skypicker.com/flights", params=parameters)
	
	try: 
		a = response2.json()['data']
		for b in a:
			ar = []
			z = datetime.utcfromtimestamp(airport['route'][0]['dTime']).strftime('%Y-%m-%d %H:%M:%S')
			print("Checking [%s] Cheapest One Way: On: %s @ £%s" % (b['cityTo'],z ,airport['price']))
			ar.append(int(b['price']))
			ar.append(tiny_url(b['deep_link']))
			ar.append(b['cityCodeTo'])
			ar.append(b['cityTo'])
			ar.append(datetime.utcfromtimestamp(b['route'][0]['dTime']).strftime('%Y-%m-%d %H:%M:%S'))
			ar.append(datetime.utcfromtimestamp(b['route'][1]['dTime']).strftime('%Y-%m-%d %H:%M:%S'))
			#print(tiny_url(b['deep_link']))
			varss.append(ar)
	except KeyError:
		continue

Sort(varss)

for x in varss:
	if x[0] == "Error":
		continue
	else:
		print("Weekend in: %s Fly Out: %s  Return: %s for £%s @ %s " % (x[3], x[4], x[5], str(x[0]), x[1]))


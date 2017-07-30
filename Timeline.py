import urllib, json
import pandas as pd
import time

millis 		= int(round(time.time() * 1000))
data 		= pd.read_csv("train.csv")
trip_id 	= data["id"].tolist()
pickup_lat 	= data["pickup_latitude"].tolist()
pickup_lon 	= data["pickup_longitude"].tolist() 
dropoff_lat	= data["dropoff_latitude"].tolist() 
dropoff_lon	= data["dropoff_longitude"].tolist() 
durations	= data["trip_duration"].tolist()
distance	= []
start_add	= []
end_add		= []
paramets	= []

for i in range(len(durations)):
	print(i)
	while(True):
		try:
			url 		= "http://maps.googleapis.com/maps/api/directions/json?origin="+str(pickup_lat[i]) + "," + str(pickup_lon[i]) + "&destination=" + str(dropoff_lat[i]) + "," + str(dropoff_lon[i]) + "&duration=" + str(durations[i])
			response 	= urllib.urlopen(url)
			data 		= json.loads(response.read())
			distance.append(data["routes"][0]["legs"][0]["distance"]["text"])
			start_add.append(data["routes"][0]["legs"][0]["start_address"])
			end_add.append(data["routes"][0]["legs"][0]["end_address"])
			params 		= "" 
			work		= data["routes"][0]["legs"][0]["steps"]
			
			for j in range(len(work)):
				params += "Step" + str(j+1) + ":{"
				params += "distance=" + work[j]["distance"]["text"] + " "
				params += "start_location=(" + str(work[j]["start_location"]["lat"]) + "," + str(work[j]["start_location"]["lng"]) + ") "
				params += "end_location=(" + str(work[j]["end_location"]["lat"]) + "," + str(work[j]["end_location"]["lng"]) + ") "
				params += "}, "

			paramets.append(params)
			break
		except  Exception, e:
			print(e)
			continue
	print("Start add len : " + str(len(start_add)) + " end add len : " + str(len(end_add)) + "paramets length : " + str(len(paramets))) 
	if(i%10==0 and i > 0):
		millis = int(round(time.time() * 1000)) - millis
		print("Uploaded 10 rows in : " + str(1.0*millis/1000) + "i = " + str(i))
		millis = int(round(time.time() * 1000))
		df = pd.DataFrame(
			{
				'trip_id' 			: trip_id[:i+1],
				'pickup_longitude' 	: pickup_lon[:i+1],
				'pickup_latitude' 	: pickup_lat[:i+1],
				'dropoff_longitude' : dropoff_lon[:i+1],
				'dropoff_latitude' 	: dropoff_lat[:i+1],
				'distance'			: distance,
				'start_address'		: start_add,
				'end_address'		: end_add,
				'parameters'		: paramets
			})

		df.to_csv("metadata.csv", index = False)
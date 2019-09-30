import flask
import requests
from flask import jsonify
def traffic_fine_check(request):
	response_parent = {}
	response_child = {}
	request_json = request.get_json()
	base_url="https://www.karnatakaone.gov.in/PoliceCollectionOfFine/FineDetails?SearchBy=REGNO&SearchValue="
	final_url="{0}{1}&ServiceCode=BPS".format(base_url,request_json['vehicleId'])
	payload = {'key': 'value'}
	response = requests.post(final_url,payload)
	#print(response.json())
	violations = response.json()['PoliceFineDetailsList']
	if(violations is not None):
		vehcile_owner = ''
		i = 0 
		all_violations = []
		for violation in violations:
		    message  = 'ViolationDate:' + violation['NoticeGenerationDate'] + ' ' + violation['ViolationTime'] + '\nPlace:' + violation['PointName'] + '\nDescription:' + violation['OffenceDescription'] + '\nFine Amount:' + violation['FineAmount']
		    vehcile_owner = violation['Name']
		    i = i + 1
		    response_child = {}
		    response_child['text'] = str(i) + ' ' + message
		    all_violations.append(response_child)
		    #print i,message,vehcile_owner

		response_child = {}
		response_child['text'] = '\nVehicle Owner for '+ request_json['vehicleId'] + ' is '+ vehcile_owner 
		all_violations.append(response_child)
		response_parent['messages'] = all_violations
		json_data = flask.json.dumps(response_parent)
		#print(json_data)
		return json_data
	else :
		response_child = {}
		response_child['text'] = '\nNo violations/records found for '+ request_json['vehicleId'] 
		all_violations = []
		all_violations.append(response_child)
		response_parent['messages'] = all_violations
		json_data = flask.json.dumps(response_parent)
		#print(json_data)
		return json_data
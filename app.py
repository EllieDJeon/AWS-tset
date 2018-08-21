from chalice import Chalice
import os
import boto3
import json
import subprocess

app = Chalice(app_name='dev30-carvi-dynamodb-chalice-dev')
# app.debug = True

# Container for all json file from GET request
OBJECTS = {}

filename = os.path.join(
	os.path.dirname(__file__), '../cf', 'dynamodb_cf.json'
)

filename2 = os.path.join(
	os.path.dirname(__file__), '../cf', 'dynamodb2_cf.json'
)

filename3 = os.path.join(
	os.path.dirname(__file__), '../cf', 'cf_iot_rule_gen_s3.json'
) 

# # Open CloudFormation for Dynamodb setup
with open(filename) as f:
	config = f.read()

with open(filename2) as f:
	config2 = f.read()

with open(filename3) as f:
	config3 = f.read()

# create an instance for CloudFormation
cf = boto3.client('cloudformation', region_name = 'us-west-2')
session = boto3.Session(region_name='us-west-2')

# create more instances for other resources
client = boto3.client('s3', region_name = 'ap-northeast-2')
paginator = client.get_paginator("list_objects")
client2 = boto3.resource('dynamodb', region_name = 'us-west-2')

origin = 'cf'
destination = 'dynamodb'

# Reference name dictionaries
cloud_env = dict({'702738637364':'dev','207840868635':'test','660909071379':'qc','043951023778':'tc'})
users =dict()
set(users.update({x:'20'}) for x in set(['AIDAIQ5BHWCJHZ3TGTP3E','AIDAJERRHDYD3YFNZTHFY',
	'AIDAI5JMJC4T5T744LQHU','AIDAIDFHZH4RPIU4WWGRS']));
set(users.update({x:'50'}) for x in set(['AIDAIF3O2S4QE4R6HJ6YQ','AIDAILUP7G25NUSUY3C76']));
set(users.update({x:'30'}) for x in set(['AIDAJLDMMQ7UIIZUJ4ELU']));


# get all credentials
current_session =session.client('sts').get_caller_identity()
user = cloud_env[current_session.get('Account')]
short_region = '{}{[0]}{}'.format(*tuple(session.region_name.split('-')))

# build a stack name
cfName = '-'.join([x for x in [user,short_region,origin,destination] if x!=None])

@app.route('/')
def welcome_page():
	return{'Message':"Welcome to CarVi Microservice Manager :) "}

# DynamoDB Welcome Page
@app.route('/dynamodb')
def describe_dynamodb():
	return{'Description':'Welcome to DynamoDB Section.'}

# Create a DynamoDB table using CloudFormation Template
@app.route('/dynamodb/create_one/{table_name}/{key}/{rcu}/{wcu}')
def create_table(table_name, key, rcu, wcu):
	# Create CF template. Pay attention to the Parameters. We define template using user input
	response = cf.create_stack(
		StackName = cfName+'-'+table_name,
		TemplateBody = config,
		Capabilities=['CAPABILITY_IAM'],
		Parameters = [
			{
	            'ParameterKey': 'tableName',
	            'ParameterValue': table_name
       	 	},
        	{
	            'ParameterKey': 'KeyName',
	            'ParameterValue': key
        	},
        	{
	            'ParameterKey': 'rcu',
	            'ParameterValue': rcu
        	},
        	{
	            'ParameterKey': 'wcu',
	            'ParameterValue': wcu
        	}
		]
	)
	return{'Result':response}

# Create a DynamoDB table using CloudFormation Template with composite primary keys
@app.route('/dynamodb/create_two/{table_name}/{keys}/{rcu}/{wcu}')
def create_table2(table_name, keys, rcu, wcu):
	# Get keys and split
	key_ls = keys.split(',')
	key = key_ls[0]
	key2 = key_ls[1]

	# Create CF template. Pay attention to the Parameters. We define template using user input
	response = cf.create_stack(
		StackName = cfName+'-'+table_name,
		TemplateBody = config2,
		Capabilities=['CAPABILITY_IAM'],
		Parameters = [
			{
	            'ParameterKey': 'tableName',
	            'ParameterValue': table_name
	   	 	},
	    	{
	            'ParameterKey': 'KeyName',
	            'ParameterValue': key
	    	},
	    	{
	            'ParameterKey': 'KeyName2',
	            'ParameterValue': key2
	    	},
	    	{
	            'ParameterKey': 'rcu',
	            'ParameterValue': rcu
	    	},
	    	{
	            'ParameterKey': 'wcu',
	            'ParameterValue': wcu
	    	}
		]
	)
	return{'Result':response}

# Delete a DynamoDB table using CloudFormation Template
@app.route('/dynamodb/delete/{table_name}')
def delete_table(table_name):
	# create an instance for CloudFormation
	cf = boto3.client('cloudformation', region_name = 'us-west-2')
	session = boto3.Session(region_name='us-west-2')	

	if not table_name:
		return{"Error":"Please to specify the table name to delete!"}
	else:
		response = cf.delete_stack(
			StackName = cfName+'-'+table_name,
		)

	return{'Result':response}


# Execute shell script to modify CF for IoT Rule (aiming for S3 bucket as an action)
@app.route('/iot/rule/create')
def create_iot_rule():
	# build a stack name (remember iot is in SEOUL region!)
	cf = boto3.client('cloudformation', region_name = 'ap-northeast-2')
	cfName = '-'.join([x for x in [user,'seoul','iot','s3'] if x!=None])

	response = cf.create_stack(
		StackName = cfName,
		TemplateBody = config3,
		Capabilities=['CAPABILITY_IAM']		
	)

	return{'Result':response}

# Insert data to DynamoDB table from S3 bucket
# @app.route('/s3/{ymd}/send_to/{table_name}/{option}')
# def send_to_db(ymd, table_name, option):
# 	# Define all attributes for each container
# 	aws_ev_name_container = ['year', 'month', 'day', 'provider', 'env', 'type', 'status', 'camera_id', 
# 	                         'hour','min', 'sec', 'millisec', 'cert', 'uuid']
# 	cv_data_name_container = ['year', 'month', 'day', 'company', 'env', 'camera_id', 'topic', 'firmware_ver', 'hour',
# 	                 'min', 'sec', 'millisec', 'cert', 'uuid']
# 	cv_shadow_name_container = ['year', 'month', 'day', 'provider', 'env', 'camera_id','type', 'status', 'shadow_stat',
# 	                            'hour', 'min', 'sec', 'millisec', 'cert', 'uuid']
# 	cv_shadow2_name_container = ['year', 'month', 'day', 'provider', 'env', 'camera_id','type', 'status',
# 	                            'hour', 'min', 'sec', 'millisec', 'cert', 'uuid']
# 	cv_job_name_container = ['year', 'month', 'day', 'provider', 'env', 'camera_id','type', 'status',
#                           'hour', 'min', 'sec', 'millisec', 'cert', 'uuid']

# 	bucket_obj_list = []
# 	if '-' in ymd:
# 		tm = ymd.split('-')

#     # set prefix in advance
# 	if '-' not in ymd: # that means ymd contains year only
# 		prefix = "{:04d}".format(int(ymd))
# 	elif len(tm) == 2: # tm contains year and month
# 		prefix = "{:04d}/{:02d}".format(int(tm[0]), int(tm[1]))
# 	else: # tm contains year, month, and day
# 		prefix = "{:04d}/{:02d}/{:02d}".format(
#             int(tm[0]), int(tm[1]), int(tm[2]))
        
# 	event ={
# 		"Bucket": "dev20-carvi-s3-iot-ap-northeast-2-topic-backup",
# 		"Prefix": "2018/08/15",
# 		"StartingToken": None
# 	}

# 	table = client2.Table(table_name)
	
# 	page_iterator = paginator.paginate(Bucket = event['Bucket'], 
#                                        Prefix = event['Prefix'],
#                                        PaginationConfig={
#                                           'MaxItems': None,
#                                           'PageSize': 1000,
#                                           'StartingToken': event["StartingToken"]
#                                       })

#     # iterate each s3 bucket content and retrieve data
# 	for page in page_iterator:
# 		bucket_obj_list += [(x["Key"]) for x in page["Contents"]]

# 	return{'hh':prefix}	
#     # parse s3 object to get json data
# 	for key_name in iter(bucket_obj_list):
# 		split_name = key_name.split('/')

# 		try:
# 			response = client.get_object(Bucket = event['Bucket'],
# 			                    Key = key_name)
# 			res = response['Body'].read()

# 			if isinstance(res, list):
# 				temp_data = res
# 				temp_dict = {'val':str(temp_data)}
# 				data = json.loads(temp_dict)
# 			else:
# 				data = json.loads(res)

# 			# create a k,v pair to put in Dynamo DB
# 			if option == 1: # put all aws-related or device status data
# 				if '$aws' in split_name: # trip data
# 					if 'shadow' in split_name: # shadow & AWS event-related
# 						# two different situations. 
# 						if len(split_name) == 15:
# 							kv_list = {k:v for k, v in zip(cv_shadow_name_container, 
# 								split_name)}
# 						else:
# 							kv_list = {k:v for k, v in zip(cv_shadow2_name_container, 
# 								split_name)}
# 					elif 'jobs' in split_name:
# 						kv_list = {k:v for k, v in zip(cv_job_name_container, 
# 							split_name)}
# 					else:
# 						kv_list = {k:v for k, v in zip(aws_ev_name_container, split_name)}

# 				kv_list['payload'] = str(data)
# 				response = table.put_item(
# 				    Item = kv_list
# 				)
# 			elif option == 2: # put each object with uuid as a primary key
# 				if not '$aws' in split_name: # trip data
# 					kv_list = {k:v for k, v in zip(cv_data_name_container, split_name)}

# 				kv_list['payload'] = str(data)
# 				response = table.put_item(
# 				    Item = kv_list
# 				)
# 		except:
# 			continue

# 	return{'Result':'success'}


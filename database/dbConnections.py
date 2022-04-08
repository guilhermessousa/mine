from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import psycopg2

"""
	MONGODB FUNCTIONS
"""
def mongoConnect(conn, db, collection):
	if(conn['user'] == '') or (conn['pass'] == ''):
		mongoURI = "mongodb://{host}:{port}/".format(
			host = conn['host'], 
			port = conn['port']
		)

	else:
		mongoURI = "mongodb://{user}:{passwd}@{host}:{port}/?authSource={authSource}".format(
			user = conn['user'],
			passwd = conn['pass'],
			host = conn['host'], 
			port = conn['port'],
			authSource = conn['authSource']
		)

	server = MongoClient(mongoURI)
	try:
		info = server.server_info()
		return server[db][collection]
	except ServerSelectionTimeoutError:
		print('Error connect database')
		exit()

"""
	POSTGRESQL FUNCTIONS
"""
def postgresqlConnect(conn, db):
	print('Connecting to:'+conn['host']+':'+conn['port'])
	try:
		connection = psycopg2.connect(user = conn['user'],
			password = conn['pass'],
			host = conn['host'],
			port = conn['port'],
			dbname = db
			)
		cursor = connection.cursor()
		return (cursor, connection)
	except (Exception, psycopg2.Error) as error:
		print ("Error while connecting to Postgresql", error)
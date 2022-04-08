import os
import sys
import pandas as pd
sys.path.insert(0,"/home/diego/projects/mine/")
from database.settings import *
from database.dbConnections import *
import json

def get_cities_with_uf(lonLat, cursor, connection):
	query = (f"SELECT name as city, acronym as uf FROM  cities WHERE st_within(st_setsrid(st_makepoint({lonLat[0]}, {lonLat[1]}),4326), geom)")
	cursor.execute(query)
	connection.commit()
	return cursor.fetchone()

def run():

    (pg_cursor, pg_connection) = postgresqlConnect(POSTGRESQL['local'], 'postgres')
    all = None
    err_docs = []
    with open('/home/diego/Downloads/source_cwshub_local.json') as f:
        all = json.load(f)

        for document in all:
            if 'location' in document:
                
                try:
                    city = get_cities_with_uf(document['location']['coordinates'], pg_cursor, pg_connection)
                    document['city'] = city[0]
                    document['uf'] = city[1]
                    # print(document['name'], document['code'], document['owner'], document['city'], document['uf'], document['location']['coordinates'])
                except:
                    err_docs.append(document)
            else:
                err_docs.append(document)
            
        df = pd.DataFrame.from_dict(all) 
        df.to_csv (r"/home/diego/Downloads/listagem.csv", index = False, header=True)    
        
        df = pd.DataFrame.from_dict(err_docs) 
        df.to_csv (r"/home/diego/Downloads/erros.csv", index = False, header=True)    
         
if __name__ == '__main__':   
    run()
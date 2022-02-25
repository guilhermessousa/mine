from settings import *
from dbConnections import *
import json

def run():

	(pg_cursor, pg_connection) = postgresqlConnect(POSTGRESQL['alertas'], 'alertas')

	with open('/home/diego/Downloads/polygons.geojson') as f:
		data = json.load(f)

		for post in data['features']:

			print("-----INICIANDO UMA NOVA INSERÇÃO------")

			cliente_idcliente = post['properties']['cliente_idcliente']

			jsonData = {
				"localidade": post['properties']['localidade'],
				"cliente": post['properties']['cliente'],
				"cliente_idcliente": cliente_idcliente,
				"localidade_idlocalidade": post['properties']['localidade_idlocalidade'],
				"geometry": str(post["geometry"]).replace("'", '"')
			}
			
			geometry = generateTheGeom(jsonData, pg_cursor, pg_connection)

			id_shape = insertIntoShapeTable(jsonData, geometry, pg_cursor, pg_connection)

			print(id_shape[0])
			print("--FIM--")
			print("")


def generateTheGeom(jsonData, cursor, connection):
	query = ("SELECT " +
			" ST_SetSRID(ST_GeomFromGeoJSON('{geometry}'), 4326) as the_geom, "+
			" ST_X(St_Centroid(ST_SetSRID(ST_GeomFromGeoJSON('{geometry}'), 4326))) as longitude,"+
			" ST_Y(St_Centroid(ST_SetSRID(ST_GeomFromGeoJSON('{geometry}'), 4326))) as latitude").format (
			geometry = jsonData["geometry"]
	)

	cursor.execute(query)
	connection.commit()

	return cursor.fetchone()


def insertIntoShapeTable(jsonData, geometry, cursor, connection):
	if ((jsonData['cliente_idcliente'] == 0) or (jsonData['cliente_idcliente'] == None)):
		idcli = 'null'
	else:
		idcli = jsonData['cliente_idcliente']

	if ((jsonData['localidade_idlocalidade'] == 0) or (jsonData['cliente_idcliente'] == None)):
		idloc = 'null'
	else:
		idloc = jsonData['localidade_idlocalidade']

	if (jsonData['cliente'] == None):
		cli = 'null'
	else:
		cli = jsonData['cliente']

	query = ("INSERT INTO localidades.poligono_shape_cliente (localidade, cliente, the_geom, cliente_idcliente, localidade_idlocalidade)"+ 
		" VALUES ('{localidade}', '{cliente}', '{the_geom}', {cliente_idcliente}, {localidade_idlocalidade})"+
		" RETURNING id").format(
			localidade = jsonData['localidade'],
			cliente = cli,
			the_geom = geometry[0],
			cliente_idcliente = idcli,
			localidade_idlocalidade = idloc
	)

	cursor.execute(query)
	connection.commit()

	return cursor.fetchone()

run()


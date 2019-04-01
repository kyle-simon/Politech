from django.apps import AppConfig
import json
import mysql.connector

class ApiConfig(AppConfig):
    name = 'api'

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="PoliDB"
    )
    mycursor = mydb.cursor()

    def update_api_votecount(self, file_name, mycursor, mydb):
        with open(file_name, 'r') as file:
            json_data = json.load(file)
        for i in json_data['features']:
            RVote= i['properties']['PRES_RVOTE']
            DVote= i['properties']['PRES_DVOTE']
            sql = "INSERT INTO api_votecount (id, num_votes, election_result_id, political_party_id) VALUES (%d, %d, %d, %d)"
            val = (1, RVote, 1, 1);
            mycursor.execute(sql,val)
            mydb.commit()

            val = (1, DVote, 1, 1);
            mycursor.execute(sql, val)
            mydb.commit()

    update_api_votecount('StateData/nh.final.json', mycursor, mydb);

import json
import mysql.connector
from mysql.connector.cursor import MySQLCursor

conn = mysql.connector.connect(
    host="ec2-100-26-189-51.compute-1.amazonaws.com",
    user="root",
    password="123456",
    database="imdb_dev"
)

cursor = conn.cursor()

#HARD CODED HERE, data will contain mssg from the Queue.
data = '{"nconst":"nm0000010","primaryName":"SOHAM MUKHERJEE","birthYear":"1899","deathYear":"1987",' \
       '"primaryProfession":"soundtrack,actor,miscellaneous"} '

json_object = json.loads(data)

sql = "INSERT INTO names (id, name, birth_year, death_year, primary_profession) " \
      "VALUES (%s,%s,%s,%s,%s) "
print()
cursor.execute(sql, (json.dumps(0), json.dumps(1), json.dumps(2), json.dumps(3)
                     , json.dumps(4)))

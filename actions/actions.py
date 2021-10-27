# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"

# lets connect to the mysql server
import mysql.connector
from mysql.connector import errorcode
import numpy as np

try:
    cnx = mysql.connector.connect(user='root', password='prasanthi', database='myprojects')
    cursor = cnx.cursor()
    query = "select * from projects"
    cursor.execute(query, multi=True)
    data = np.array(cursor.fetchall())

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()

names, descs, links, mldl = [], [], [], []

for i in range(data.shape[0]):
    names.append(data[i][0])
    descs.append(data[i][1])
    links.append(data[i][2])
    mldl.append(data[i][3])

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionMyProjects(Action):

    def name(self) -> Text:
        return "my_projects"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ml = []
        dl = []
        for i in range(6):
            if mldl[i] == 'ml':
                ml.append(names[i])
            else:
                dl.append(names[i])
        dispatcher.utter_message(text=f"My Machine learning projects are: \n{ml} \n"
                                      f"My Deep Learning Projects are: \n{dl}")

        return []


import rasa
print(rasa.__version__)
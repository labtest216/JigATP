import pymongo
import json
import time
from datetime import datetime
from datetime import timedelta


class Reporter:
    query = None
    answer = []

    def __init__(self, connection, db, collection):
        # Open db connection.
        self.connection = pymongo.MongoClient(str(connection))
        self.db = self.connection[str(db)]
        self.collection = self.db[collection]

    def print_query(self):
        for x in self.query:
            self.answer.append(x)
            print(x)
        return self.answer

    def store_on_db(self, data_to_store):
        # Store data on db in collection.
        self.collection.insert_one(data_to_store)

    def get_last_test_reports_by_days(self, days):
        days = timedelta(days=days)
        last_days = datetime.now() - days
        self.query = self.db.test_report.find({"test_start": {"$gt": str(last_days)}})
        return self.print_query()

    def get_test_reports_by_date(self, start_date, end_date, test_name):
        start = str(start_date).split(",")
        end = str(end_date).split(",")
        start_ = datetime(int(start[0]), int(start[1]), int(start[2]), int(start[3]))
        end_ = datetime(int(end[0]), int(end[1]), int(end[2]), int(end[3]))

        self.query = self.db.test_report.find({"$and": [
                                                    {"test_name": test_name},
                                                    {"test_start": {"$gt": str(start_)}},
                                                    {"test_start": {"$lt": str(end_)}}
                                                    ]})
        return self.print_query()

    def get_test_reports_by_stud_id(self, stud_id, test_name=None):

        if test_name is None:
            self.query = self.db.test_report.find({"stud_id": stud_id})
        else:
            self.query = self.db.test_report.find({"$and": [
                                                        {"stud_id": stud_id},
                                                        {"test_name": test_name}
                                                        ]})
        return self.print_query()

    def query(self, string_query):
        self.query = self.db.test_report.find(string_query)
        return self.print_query()


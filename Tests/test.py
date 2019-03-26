
import time
import datetime
import logging
from Mongo.test_reporter import Reporter
from Sniffer.sniffer import Sniffer
from RelayBoard.denkovi16 import Denkovi16
from Sensor.LDA_GPS import LedAnalyzer
from Motor.motor import Motor
from GetWay.getway import Getway
from Mongo.histogram import Histogram
from config import *
from util import *


class Test:

    # Init test equipment.
    name = str(type().__name__)
    histo = Histogram()
    snif = Sniffer()
    motor = Motor()
    rb = Denkovi16()
    gw = Getway()
    lda = LedAnalyzer()
    reporter = Reporter(connection, db, col)

    # Init test values.
    pre_value = 0
    post_value = 0
    delta = 0
    result = 0
    status = 'FAIL'
    stud_id = 2

    def __init__(self):
        self.test_start_unix = time.time()
        self.test_start = datetime.now()
        print(self.test_start)

        # Create sniffer log folder.
        if not os.path.isdir(log_path + self.test_name()):
            os.mkdir(log_path + self.test_name())

        # Get test cfg params.
        test_cfg = self.get_test_cfg(str(self.test_name()))

        self.limit_low = test_cfg.limit_low
        self.limit_high = test_cfg.limit_high
        self.sniffer_parser = test_cfg.sniffer_parser
        self.sniffer_lines = test_cfg.sniffer_lines

        # Test setup.
        self.setup()
        # Test Process.
        self.test(self.limit_low, self.limit_low)
        # Test Close.
        self.close()
        self.report_to_db()

    def check_test_limits(self):
        self.delta = self.post_value - self.pre_value
        self.result = check_limits(self.limit_low, self.limit_high, self.delta)

    def test_name(self):
        name = str(type(self).__name__)
        return name

    def log_pre(self):
        log = log_path + self.test_name() + '\\pre.txt'
        return log

    def log_post(self):
        log = log_path + self.test_name() + '\\post.txt'
        return log

    def logger(self): pass

    def print_result(self):
        if self.result:
            self.status = 'PASS'
        else:
            self.status = 'FAIL'

        debug_print = "test_name="+self.test_name()+" post_value=" + str(self.post_value) + \
                      " pre_value=" + str(self.pre_value) + " delta=" + \
                        str(self.delta) + " limit_low=" + str(self.limit_low) + " limit_high=" + str(self.limit_high)
        dprint(debug_print+"\n"+"status="+self.status)
        print("-------------------------_" + str(self.test_name()) + "_test_end_-------------------------")

    def report_to_db(self):
        self.test_end = time.time()
        self.test_time = self.test_end - self.test_start_unix

        test_report = {"test_time": self.test_time, "test_start": str(self.test_start),
                       "test_start_unix": self.test_start_unix, "test_name": self.test_name(),
                       "test_status": self.status, "test_result": self.result,
                       "test_limit_low": self.limit_low, "test_limit_high": self.limit_high,
                       "stud_id": self.stud_id}

        self.reporter.store_on_db(test_report)
        #self.reporter.get_test_reports_by_date("2019,1,1,5", "2019,3,12,18", 'PcbeTemp')
        self.get_test_histogram("2019,3,12,12", "2019,3,12,18", 'PcbeTemp')


    def setup(self):
        print("-------------------------_" + str(self.test_name()) + "_test_start_-------------------------")


    def test(self): pass

    def close(self):
        self.print_result()

    def get_test_cfg(self, test_name):
        # Get test cfg params.
        test_cfg_obj = get_class("Tests.cfg_tests." + str(test_name) + "TestParams")
        test_cfg = test_cfg_obj()
        return test_cfg

    def get_test_histogram(self, start_date, end_date, test_name):
        x_values = []
        test_cfg = self.get_test_cfg(test_name)
        self.reporter.answer = self.reporter.get_test_reports_by_date(start_date, end_date, test_name)
        print(self.reporter.answer)
        for x in self.reporter.answer:
            x_values.append(x["test_result"])

        self.histo.x_value = x_values
        self.histo.limit_high = test_cfg.limit_high
        self.histo.limit_low = test_cfg.limit_low
        self.histo.title = test_name
        self.histo.x_label = test_cfg.result_unit
        self.histo.y_label = "Units"
        self.histo.show()



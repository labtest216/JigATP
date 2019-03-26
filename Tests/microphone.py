from util import *
from Tests.test import Test
from Tests.cfg_tests import *


class PcbvTemp(Test):

    def __init__(self):
        super().__init__()

    def setup(self):
        self.rb.buzzer_off()
        self.snif.read(self.sniffer_lines, self.log_pre())

    def test(self, limit_low, limit_high):
        self.pre_value = find_avg_value_from_file(self.log_pre(), self.sniffer_parser)
        self.rb.buzzer_on()
        self.snif.read(self.sniffer_lines, self.log_post())
        self.post_value = find_avg_value_from_file(self.log_post(), self.sniffer_parser)
        self.check__test_limits()


    def close(self):
        self.rb.buzzer_off()
        self.print_result()





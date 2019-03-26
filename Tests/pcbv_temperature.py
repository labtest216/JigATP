from util import *
from Tests.test import Test
from Tests.cfg_tests import *


class PcbvTemp(Test):

    def __init__(self):
        super().__init__()

    def setup(self):
        super().setup()
        self.rb.light1_off()
        self.snif.read(self.sniffer_lines, self.log_pre())

    def test(self, limit_low, limit_high):
        self.pre_value = find_avg_value_from_file(self.log_pre(), self.sniffer_parser)
        self.rb.light1_on()
        self.snif.read(self.sniffer_lines, self.log_post())
        self.post_value = find_avg_value_from_file(self.log_post(), self.sniffer_parser)
        self.check_test_limits()

    def close(self):
        self.rb.light1_off()
        super().close()





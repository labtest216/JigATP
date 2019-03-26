from util import *
from Tests.test import Test
from Tests.cfg_tests import *

class PcbeTemp(Test):

    def __init__(self):
        super().__init__()

    def setup(self):

        self.rb.light1_off()
        self.snif.read(100, self.log_pre())

    def test(self, limit_low, limit_high):
        self.pre_value = find_avg_value_from_file(self.log_pre(), self.sniffer_parser)
        self.rb.light1_on()
        self.snif.read(100, self.log_post())
        self.post_value = find_avg_value_from_file(self.log_post(), self.sniffer_parser)
        self.delta = self.post_value - self.pre_value
        self.result = check_limits(limit_low, limit_high, self.delta)

    def close(self):
        self.rb.light1_off()
        super().close()
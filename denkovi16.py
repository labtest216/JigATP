#!/usr/bin/env python
from serial import Serial
from RelayBoards.relayboards import RelayBoard


class Denkovi16(RelayBoard):
    all_switches_off = "off//"
    relay_card_test = "ask//"
    switches_off = {"1": "01-//", "2": "02-//", "3": "03-//", "4": "04-//", "5": "05-//", "6": "06-//", "7": "07-//",
                    "8": "08-//", "9": "09-//", "10": "10-//", "11": "11-//", "12": "12-//", "13": "13-//",
                    "14": "14-//", "15": "15-//", "16": "16-//"}
    switches_on = {"1": "01+//", "2": "02+//", "3": "03+//", "4": "04+//", "5": "05+//", "6": "06+//", "7": "07+//",
                   "8": "08+//", "9": "09+//", "10": "10+//", "11": "11+//", "12": "12+//", "13": "13+//",
                   "14": "14+//", "15": "15+//", "16": "16+//"}

    def __init__(self, cfg):
        super().__init__(cfg)
        self.com = Serial(self.cfg["interface"]["com"], self.cfg["interface"]["br"], 8, 'N', 1)
        self.init_com()

    def init_com(self):
        if self.com.is_open:
            self.dprint("Communication with relay board open.")
            self.init_relay_card()
        else:
            self.dprint("Com can not open, Communication with relay board fail.")



    def init_board(self):
        if self.send_and_wait(self.all_switches_off, "off") == 0:
            if self.send_and_wait(self.relay_card_test, "\x00\x00") == 0:
                self.dprint(f_name() + " pass")
                return 0
            else:
                self.dprint(f_name() + " fail")
                return -1
        else:
            self.dprint(f_name() + " fail")
            return -1

        # Switch On =1, Switch Off=0 .

    def send_and_wait(data_to_send, data_to_get):
        self.com.write(data_to_send)




    def set_switch(self, switch_num, mode):
        assert 1 <= switch_num <= self.num_of_relay, " No switch like this"
        if mode == 1:  # Switch On.
            feedback = self.switches_on[str(switch_num)]
            if self.send_and_wait(self.switches_on[str(switch_num)], feedback) == 0:
                self.dprint(f_name() + " number " + str(switch_num) + " on pass")
                return 0
            else:
                self.dprint(f_name() + " fail")
                return -1

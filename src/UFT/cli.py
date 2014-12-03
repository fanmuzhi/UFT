#!/usr/bin/env python
# encoding: utf-8
"""command line interface for UFT
"""
__version__ = "0.1"
__author__ = "@boqiling"
from UFT.channel import ChannelStates, Channel
import time
import argparse

# pass args
def parse_args():
    parser = argparse.ArgumentParser(description="Universal Functional Test "
                                                 "Program for Agigatech PGEM. "
                                                 "@boqiling 2014.")

    parser.add_argument('-s', dest='singlevalue', action='store', help='store a value')
    parser.add_argument('-v', dest='verbose', action='store_true', help='verbose', default=False)
    parser.add_argument('word', action='store', help='word to action')

    args = parser.parse_args()
    return args

# cli command to prepare database

# cli command to synchronize the dut config


# cli command to debug hardware

# cli command to run single test
def single_test():

    barcode = "AGIGA9601-002BCA02143500000002-04"
    ch = Channel(barcode_list=[barcode, "", "", ""], channel_id=0,
                 name="UFT_CHANNEL")
    ch.start()

    ch.queue.put(ChannelStates.INIT)
    ch.queue.put(ChannelStates.CHARGE)
    ch.queue.put(ChannelStates.LOAD_DISCHARGE)
    ch.queue.put(ChannelStates.EXIT)

    while(ch.is_alive):
        print "test progress: {0}%".format(ch.progressbar)
        time.sleep(2)

# cli command to generate test reports

# cli command to generate dut charts

# calculate capacitor
# t = (C * (V0 - V1)) / I                # constant current
# C = (I * t) / (V0 - V1)


# t = (0.5 * C * (V0**2 - V1**2) / P     # constant power
# t = - C * R * ln(V1 / V0)              # constant resistance

if __name__ == "__main__":
    single_test()

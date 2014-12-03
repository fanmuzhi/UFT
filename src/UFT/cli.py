#!/usr/bin/env python
# encoding: utf-8
"""command line interface for UFT
"""
__version__ = "0.1"
__author__ = "@boqiling"
from UFT.channel import ChannelStates, Channel
from UFT import config
import time
import argparse

# pass args
def parse_args():
    parser = argparse.ArgumentParser(description="Universal Functional Test "
                                                 "Program for Agigatech PGEM. "
                                                 "@boqiling 2014.")
    parser.add_argument('-l', '--list-config',
                        dest='listconfig',
                        action='store_true',
                        help='list current configuration of UFT',
                        default=False)
    parser.add_argument('--run',
                        dest='run',
                        action='store_true',
                        help='run test automatically',
                        default=False)
    parser.add_argument('--syncdb',
                        dest='syncdb',
                        action='store_true',
                        help='synchronize the configuration file with '
                             'configuration database',
                        default=False)
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help='start debug hardware and hardware connections',
                        default=False)
    parser.add_argument('-s', '--silent',
                        dest='silent',
                        action='store_true',
                        help='do not print information on the screen',
                        default=False)

    args = parser.parse_args()
    return args

# cli command to prepare database

# cli command to synchronize the dut config


# cli command to debug hardware

# cli command to run single test
def single_test():
    #barcode = "AGIGA9601-002BCA02143500000002-04"
    barcode_list = []
    for i in range(config.TOTAL_SLOTNUM):
        barcode_list.append(raw_input("please scan the barcode of dut{"
                                      "0}".format(i)) or "")
    ch = Channel(barcode_list=barcode_list, channel_id=0,
                 name="UFT_CHANNEL")
    ch.auto_test()
    while(ch.is_alive):
        print "test progress: {0}%".format(ch.progressbar)
        time.sleep(2)

#TODO cli command to generate test reports

#TODO cli command to generate dut charts

def main():
    args = parse_args()
    if args.silent:
        pass
    if args.listconfig:
        pass
    if args.debug:
        pass
    if args.syncdb:
        pass
    if args.run:
        single_test()

if __name__ == "__main__":
    main()

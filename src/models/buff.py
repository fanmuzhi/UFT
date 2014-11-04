'''
Created on Jul 2, 2013
Read config.xml to load path, size of vpd and spd.
load raw *.ebf file and *.bin file.
Rewrite the config list to buffer(ex:YY,WW,VV,ID...) and
return the buffer content.
@author: mzfa
'''
import os
import inspect
import struct
import simplexml

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
CONFIG = path + '/config.xml'


class BufferContructException(Exception):
    pass


def load_bin_file(path):
    """read a file and transfer to a binary list
    """
    datas = []
    f = open(path, 'rb')
    s = f.read()
    for x in s:
        rdata = struct.unpack("B", x)[0]
        datas.append(rdata)
    return datas


def read_config(name, revision):
    val = None
    if not os.path.exists(CONFIG):
        print CONFIG
        raise BufferContructException("config file doesn't find.")

    with open(CONFIG, "rb") as f:
        s = f.read()

    config = simplexml.loads(s)

    for project in config["Project"]:
        val = project["Project"]
        if (val["name"]==name and val["revision"]==revision):
            return val
    if val is None:
        raise BufferContructException("no matched config found.")


def load_vpd(barcode):
    buff = BufferConstruct()
    conf = read_config(barcode['PN'], barcode['RR'])
    vpd_en = conf.find('vpd_enable').text
    if(int(vpd_en) != 1):
        raise error.VPD_DISABLED
    else:
        vpd_buff = buff.vpd_buffer(barcode, conf)
    return vpd_buff


def load_spd(barcode):
    buff = BufferConstruct()
    conf = read_config(barcode['PN'], barcode['RR'])
    spd_en = conf.find('spd_enable').text
    if(int(spd_en) != 1):
        raise error.SPD_DISABLED
    else:
        spd_buff = buff.spd_buffer(barcode, conf)
    return spd_buff


class BufferConstruct(object):
    '''
    '''

    def __accii_list(self, string):
        strlist = list(string)
        for i in range(len(strlist)):
            strlist[i] = ord(strlist[i])
        return strlist

    def __bcd_code(self, string):
        bcd = ((int(string[-2]) & 0xff) << 4) | (int(string[-1]) & 0xff)
        return bcd

    def vpd_buffer(self, barcode, conf):
        '''
        vpd buffer rewrite content position
        ID:     0x287--0x28E 8Bytes(647--654 in buff list)
        MFDATE: 0X291--0X294 4Bytes(657--660 in buff list),
                the content in MFDATE IS YYWW
        ENDUSR: 0X295--0X296 2Bytes(661--662 in buff list),
                the content in ENDUSR is VV
        '''
        vpd_file = str(conf.find('vpd_file').text)
        vpd_size = int(conf.find('vpd_size').text)
        buffebf = load_bin_file(vpd_file)

        # rewrite buffer content here
        # put buffer into self.vpd_buff
        idlist = self.__accii_list(barcode['ID'])
        yywwlist = self.__accii_list(str(barcode['YY']) + str(barcode['WW']))
        vvlist = self.__accii_list(barcode['VV'])
        buffebf[647:647 + len(idlist)] = idlist
        buffebf[657:657 + len(yywwlist)] = yywwlist
        buffebf[661:661 + len(vvlist)] = vvlist
        return buffebf

    def spd_buffer(self, barcode, conf):
        '''
        spd buffer rewrite content position
            VV:     0x077 1Bytes(119 in buff list), VV 04 == 0x04
            YY:     0x078 1Bytes(120 in buff list), year 12 == 0x12
            WW:     0x079 1Bytes(121 in buff list), week 51 == 0x51
            ID:     0x07A--0x07D 4Bytes(122--125 in buff list),
                      ex:  ID'12345678' => 0x7A:0x78;
                                           0x7B:0x56;
                                           0x7C:0x34;
                                           0x7D:0x12
        '''
        spd_file = str(conf.find('spd_file').text)
        spd_size = int(conf.find('spd_size').text)
        buffbin = load_bin_file(spd_file)
        # rewrite buffer content here
        # put buffer into self.spd_buff
        buffbin[119] = self.__bcd_code(barcode['VV'])
        buffbin[120] = self.__bcd_code(barcode['YY'])
        buffbin[121] = self.__bcd_code(barcode['WW'])
        buffbin[122] = self.__bcd_code(barcode['ID'][6:8])
        buffbin[123] = self.__bcd_code(barcode['ID'][4:6])
        buffbin[124] = self.__bcd_code(barcode['ID'][2:4])
        buffbin[125] = self.__bcd_code(barcode['ID'][0:2])
        return buffbin


if __name__ == "__main__":
    #barcode = {
    #    'PN': 'AGIGA8601-400BCA',
    #    'RR': '10',
    #    'VV': '04',
    #    'YY': '13',
    #    'WW': '28',
    #    'ID': '12345678'
    #}
    #result = load_vpd(barcode)
    #if(result is not None):
    #    print result
    #else:
    #    print "Error: value is none"

    from pprint import pprint
    pprint(read_config("AGIGA8601-400BCA", "10"))

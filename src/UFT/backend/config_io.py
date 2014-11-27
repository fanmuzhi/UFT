#!/usr/bin/env python
# encoding: utf-8
"""Description: sync the configuration db with single xml files.
load configuration from xml file, insert to db.
or load configuration from db, save to xml file.
"""

__version__ = "0.1"
__author__ = "@boqiling"

from simplexml import loads, dumps
from configuration import PGEMConfig, TestItem
from session import SessionManager
import logging
import os
import re

logger = logging.getLogger(__name__)


class BackendException(Exception):
    pass


def save_config(config, directory="."):
    """
    save PGEMConfig in dict format to xml
    :param config: dict to save to xml
    :param directory: directory to store all the xml files
    :return: xml string
    """
    filename = config["partnumber"] + "-" + config["revision"] + ".xml"
    filepath = os.path.join(directory, filename)
    result = dumps(config, "entity")
    with open(filepath, "wb") as f:
        f.truncate()
        f.write(result)
    return result


def load_xml(filepath):
    """
    load PGEMConfig in dict format from xml file.
    :param filepath: file to load config
    :return: config dict
    """
    with open(filepath) as f:
        result = loads(f.read())
        return result


def load_config(dburi, partnumber, revision):
    """
    :param dburi:  database uri, eg. "sqlite:///config.db"
    :param partnumber: partnumber of DUT, eg. "AGIGA9601-002BCA"
    :param revision: revision of DUT, eg."04"
    :return: PGEMConfig object
    """
    sm = SessionManager()
    sess = sm.get_session(dburi)
    pgem_config = sess.query(PGEMConfig).filter(
        PGEMConfig.partnumber == partnumber,
        PGEMConfig.revision == revision,
    ).first()
    if pgem_config is None:
        raise BackendException(partnumber +
                               " is not found in configuration database")
    logger.debug(pgem_config.to_dict())
    sess.close()
    return pgem_config


def load_test_item(config, itemname):
    """
    load misc test items from config object with item name.
    :param config: config object
    :param itemname: item name in string
    :return: dict of test items configuration
    """
    for item in config.testitems:
        if(item.name != itemname):
            continue
        miscs = item.misc.split(";")
        regex = re.compile("(?P<key>[^=]+)=(?P<value>.+)")
        this_misc = {}
        for misc in miscs:
            r = regex.search(misc)
            if r:
                result = r.groupdict()
                this_misc[result["key"]] = result["value"]
        return dict(this_misc.items() + item.to_dict()[itemname].items())


def sync_config(dburi, directory):
    """
    synchronize the database with xml files in specified directory
    :param dburi: database uri
    :param directory: directory to store the xml fils
    :return: None
    """

    sm = SessionManager()
    sess = sm.get_session(dburi)
    sm.prepare_db(dburi, [PGEMConfig, TestItem])

    # file to db
    file_list = []
    for root, folder, files in os.walk(directory):
        for f in files:
            #if(f.endswith(".xml") or f.endswith(".XML")):
            regex = re.compile(r"AGIGA\d{4}\-\d{3}\w{3}-\d{2}\.xml",
                               re.IGNORECASE)
            if(regex.match(f)):
                file_list.append(os.path.join(root, f))
    for f in file_list:
        config = load_xml(f)
        logger.debug(config)

        result = sess.query(PGEMConfig).filter(
                        PGEMConfig.partnumber == config["partnumber"],
                        PGEMConfig.revision == config["revision"]).first()
        if result:
            pgem_config = result
            pgem_config.testitems = []
        else:
            pgem_config = PGEMConfig()
        for k, v in config.items():
            if k != "testitems" and k != "TESTITEMS":
                setattr(pgem_config, k.lower(), v)
            else:
                items = v
                for tk, tv in items.items():
                    test_item = TestItem()
                    setattr(test_item, "NAME".lower(), tk)
                    for dk, dv in tv.items():
                        setattr(test_item, dk.lower(), dv)
                    pgem_config.testitems.append(test_item)
        logger.debug(pgem_config)
        try:
            sess.add(pgem_config)
            sess.commit()
        except Exception as e:
            sess.rollback()
            raise e
        finally:
            sess.close()

    # db to file
    for config in sess.query(PGEMConfig).all():
        save_config(config.to_dict(), directory)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    db = "sqlite:///configuration.db"
    sync_config(db, "./")


    #crystal = load_config(db, partnumber="AGIGA9601-002BCA",
    #                      revision="04")
    #print crystal.PARTNUMBER
    #print crystal.REVISION
    #print crystal.to_dict()
    #print save_config(crystal.to_dict())
    #print load_xml("./AGIGA9601-002BCA-04.xml")

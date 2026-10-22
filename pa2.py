#Taydan Brown 041160680
import sys
import json
import xml.etree.ElementTree as ET
import yaml

class BadFile(Exception):
    """Raise exception if file input is wrong or missing"""
    pass

class Device():
    """Creates device instances for easy organization"""
    pass

def main():
    """Main function to run everything"""

    dev_di = {}
    dev_ids = []
    #open files using "with open"
    inventory_path = sys.argv[1]
    policy_path = sys.argv[2]
    with open(inventory_path, "r", encoding = "utf-8") as f:
        tree = ET.parse(f)
        root = tree.getroot()

        for devs in root.findall("device")
            #get devices id, key = dev id, 
            # value = class instance of dev
            dev_id = devs.get("id")
            if dev_id and dev_id.strip() != "":
                dev_ids.append(dev_id)
                dev_di[dev_id] = Device(devs)
            





    
    #no bare excepts 
    #yaml safe load
    #minimum 5 commits 1/5 done
    #one branch 1/1 branches - device class
    #gitignore 0/1 added
    pass


if __name__ == "__main__":
    main()
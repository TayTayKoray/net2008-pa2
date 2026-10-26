#Taydan Brown 041160680
import sys
import json
import xml.etree.ElementTree as ET
import yaml

class BadFile(Exception):
    """Raise exception if file input is wrong or missing"""
    #add error calls in the read sections
    pass

class Device():
    """Creates device instances for easy organization"""
    def __init__(self,devs):
        """Intializes the variables for device class"""
        self.id = devs.id
        self.role = devs.role
        self.os = devs.os
        self.owner = devs.owner
        self.intf = []
        for intfs in devs.findall("interface"):
            self.intf.append({
                "name": intfs.get("name"),
                "status": intfs.get("status")
            })
        self.err = []

    def polcheck(self, policy):
        """Checks if policy error in class"""
        if self.id == None:
            return
        
        if self.role == "switch":
            if policy["switch"] != self.os:
                self.err.append({
                    "device": self.id,
                    "type": "os_outdated",
                    "found": self.os,
                    "required": policy["switch"]
                    })
        elif self.role == "router":
            if policy["router"] != self.os:
                self.err.append({
                    "device": self.id,
                    "type": "os_outdated",
                    "found": self.os,
                    "required": policy["router"]
                })
        elif self.role == "firewall":
            if policy["firewall"] != self.os:
                self.err.append({
                    "device": self.id,
                    "type": "os_outdated",
                    "found": self.os,
                    "required": policy["firewall"]
                })
        else:
            self.err.append({
                "device": self.id,
                "type": "unknown_role",
                "role": self.role
            })

        if policy["require_owner"] == True:
            if self.owner == None:
                self.err.append({
                    "device": self.id,
                    "type": "missing_owner"
                })

        downs = 0
        for infs in self.interf:
            if infs["satus" == "down"]:
                downs += 1
        if downs > policy["max_down_interfaces"]:
            self.err.append({
                "device": self.id,
                "type": "too_many_down",
                "down": downs
            })
        if not self.err:
            self.compliant = True

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

    with open(policy_path, "r", enconding = "utf-8") as f:
        policy = yaml.safe_load()
        for devs in dev_di:
            devs.polcheck(policy)

    #add writing and outputs
            





    
   
    #gitignore 0/1 added
    pass


if __name__ == "__main__":
    main()
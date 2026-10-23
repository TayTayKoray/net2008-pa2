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
            if policy["firewall"] != self.id:
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
            if self.interf[] == "down":
                downs += 1
        if downs > policy["max_down_interfaces"]:
            self.err.append({
                "device": self.id,
                "type": "too_many_down",
                "down": downs
            })


    def formout(self):
        """Formats variables and info for json writing"""

        return 

def main():
    """Main function to run everything"""

    #open files using "with open"
    #no bare excepts 
    #yaml safe load
    #minimum 5 commits 0/5 done
    #one branch 0/1 branches
    #gitignore 0/1 added
    pass


if __name__ == "__main__":
    main()
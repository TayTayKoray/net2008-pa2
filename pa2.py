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
        self.id = devs.get("id")
        self.role = devs.get("role")
        self.os = devs.get("os")

        owns = devs.find("owner")
        if owns is not None:
            self.owner = owns.text.strip()
        else:
            self.owner = None
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
            if infs.get("satus") == "down":
                downs += 1
        if downs > policy.get("max_down_interfaces"):
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
    inventory_path = sys.argv[1]
    policy_path = sys.argv[2]
    try:
        with open(inventory_path, "r", encoding = "utf-8") as f:
            tree = ET.parse(f)
            root = tree.getroot()

            for devs in root.findall("device"):
                dev_id = devs.get("id")
                if dev_id and dev_id.strip() != "":
                    dev_ids.append(dev_id)
                    dev_di[dev_id] = Device(devs)
        raise BadFile(f"XML file")
    except Exception as e:
        print(f"Error with loading {e}")
        sys.exit(1)

    try:
        with open(policy_path, "r", encoding = "utf-8") as f:
            policy = yaml.safe_load()
            for devo_s in dev_di:
                devs.polcheck(policy)
        raise BadFile(f"Yaml file")
    except Exception as e:
        print(f"Error with loading {e}")
        sys.exit(1)
  
    vios = []
    compl = []
    for devo_s in dev_di.values():
        if devo_s.err:
            vios.extend(devo_s.err)
        if getattr(devo_s, "compliant", False):
            compl.append(devo_s.id)

    rol_di = {}
    for devo_s in dev_di.values():
        role = devo_s.role
        if role:
            rol_di[role] = rol_di.get(role, 0) + 1

    intrf_di = {
        "up": 0,
        "down": 0,
        "other": 0
    }  
    for devo_s in dev_di.values():
        for intrf in devo_s.intf:
            status = intrf.get("status")
            if status in intrf_di:
                intrf_di[status] += 1
            else:
                intrf_di["other"] += 1

    xml_dev = len(root.findall("device"))
    skip_dev = xml_dev - len(dev_di)

    audit = {
        "site": root.get("site"),
        "total_decies": len(dev_di),
        "skipped_devices": skip_dev,
        "roles": rol_di,
        "interfaces": intrf_di,
        "violations": vios,
        "compliant": sorted(compl)
    }

    with open("audit.json", "w", encoding = "utf-8") as f:
        json.dump(audit, f, indent = 4)


if __name__ == "__main__":
    main()
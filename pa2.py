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
        if owns is not None and owns.text and owns.text.strip() != "":
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
        min_o = policy.get("min_os") or {}
        sw = min_o.get("switch")
        rt = min_o.get("router")
        fw = min_o.get("firewall")
        
        if self.role == "switch":
            if sw is not None and sw > self.os:
                self.err.append({
                    "device": self.id,
                    "type": "os_outdated",
                    "found": self.os,
                    "required": sw
                    })
        elif self.role == "router":
            if rt is not None and rt > self.os:
                self.err.append({
                    "device": self.id,
                    "type": "os_outdated",
                    "found": self.os,
                    "required": rt
                })
        elif self.role == "firewall":
            if fw is not None and fw > self.os:
                self.err.append({
                    "device": self.id,
                    "type": "os_outdated",
                    "found": self.os,
                    "required": fw
                })
        elif "min_os" in policy:
            self.err.append({
                "device": self.id,
                "type": "unknown_role",
                "role": self.role
            })

        if policy.get("require_owner") == True:
            if self.owner == None:
                self.err.append({
                    "device": self.id,
                    "type": "missing_owner"
                })

        downs = 0
        for infs in self.intf:
            if infs.get("status") == "down":
                downs += 1
        if "max_down_interfaces" in policy:
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
    if len(sys.argv) != 3:
        print("usage: arguments must equal 2, policy in yaml, devices in xml")
        sys.exit(2)
    inventory_path = sys.argv[1]
    policy_path = sys.argv[2]
    try:
        try:
            with open(inventory_path, "r", encoding = "utf-8") as f:
                tree = ET.parse(f)
                root = tree.getroot()

                for devs in root.findall("device"):
                    dev_id = devs.get("id")
                    if dev_id and dev_id.strip() != "":
                        dev_di[dev_id] = Device(devs)
        except Exception as e:
            raise BadFile(f"Error with inventory using {inventory_path}")

        try:
            with open(policy_path, "r", encoding = "utf-8") as f:
                policy = yaml.safe_load(f)
                if policy is None:
                    policy = {}
                if not isinstance(policy, dict):
                    raise BadFile(f"Policy error with {policy_path}")
        except Exception as e:
            raise BadFile(f"{e}")
        
    except BadFile as e:
        print(f"{e}")
        sys.exit(1)

    for devo_s in dev_di.values():
        devo_s.polcheck(policy)

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
        "total_devices": len(dev_di),
        "skipped_devices": skip_dev,
        "roles": rol_di,
        "interfaces": intrf_di,
        "violations": vios,
        "compliant": sorted(compl)
    }

    with open("audit.json", "w", encoding = "utf-8") as f:
        json.dump(audit, f, indent = 4)
    print("Audit Complete")


if __name__ == "__main__":
    main()
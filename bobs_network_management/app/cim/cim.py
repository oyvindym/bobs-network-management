import os
import subprocess
import xml.etree.ElementTree as ET

class CimParser(object):

    def __init__(self, wbemtarget):
        self.wbemtarget = wbemtarget

    def execute(self, command):
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        return err

    def wbemRequest(self, operation, args):
        command = "wbemcli -dx -nl %s %s:%s" % (operation, self.wbemtarget, args)
        return self.execute(command)

    def wbemResponseAsXml(self, operation, args):
        rawData = self.wbemRequest(operation, args)
        xmlStart = 'From server: <?xml version="1.0" encoding="utf-8" ?>'
        strings = rawData.split(xmlStart)
        xml = '<?xml version="1.0" encoding="utf-8" ?>' + strings[1]
        return xml

    def getIPInterfaces(self):
        args = "CIM_IPProtocolEndpoint"
        lists = self.getPropertyListsFromWBEM(args)
        interfaces = []
        for l in lists:
            interfaceInfo = self.getPropertyValues(l, ["Name", "IPv4Address", "SubnetMask"])
            interfaces.append(interfaceInfo)

        return interfaces

    def getOperatingSystemsData(self):
        args = "CIM_OperatingSystem"
        lists = self.getPropertyListsFromWBEM(args)
        if len(lists) > 1:
            raise IndexError("Too many operative systems!")
        version = self.getPropertyValue(lists[0], "Version")
        return version

    def getSystemInformation(self):
        sysInfo = SystemInformation(self.getOperatingSystemsData())
        interfaces = self.getIPInterfaces()
        for interface in interfaces:
            sysInfo.addInterface(Interface(interface[0], interface[1], interface[2]))

        return sysInfo

    def getPropertyListsFromWBEM(self, args):
        lists = []
        xml = self.wbemResponseAsXml("ein", args)
        instances = self.getInstancesFromXml(xml)
        for instance in instances:
            keybinding = self.getKeyBindingsString(instance)
            instanceXml = self.getInstanceFromWBEM(keybinding)
            propertyList = self.getPropertyListFromXml(instanceXml)
            lists.append(propertyList)
        return lists

    def getInstanceFromWBEM(self, key):
        return self.wbemResponseAsXml("gi", key)

    def getPropertyListFromXml(self, xml):
        root = self.getXmlRoot(xml)
        propertyTree = root.findall("./MESSAGE/SIMPLERSP/IMETHODRESPONSE/IRETURNVALUE/INSTANCE/")
        return propertyTree

    def getPropertyValue(self, propertyList, propertyName):
        for element in propertyList:
            if element.attrib['NAME'] == propertyName:
                return element.getchildren()[0].text

    def getPropertyValues(self, propertyList, propertyNames):
        properties = []
        for name in propertyNames:
            properties.append(self.getPropertyValue(propertyList, name))
        return properties

    def getInstancesFromXml(self, xml):
        root = self.getXmlRoot(xml)
        instances = root.findall("./MESSAGE/SIMPLERSP/IMETHODRESPONSE/IRETURNVALUE/")
        return instances

    def getKeyBindingsString(self, instance):
        keybinding = instance.attrib.values()[0] + "."
        for key in instance:
            keybinding += key.attrib.values()[0] + "="
            for child in key:
                keybinding += '"' + child.text + '"' + ","
        return "'" + keybinding.strip(',') + "'"


    def getXmlRoot(self, string):
        return ET.fromstring(string)

class SystemInformation(object):
    def __init__(self, sysDescr):
        """
        Initialize a system information class
        :input sysDescr:
        """
        self.sysDescr = sysDescr
        self.interfaces = []

    def addInterface(self, interface):
        """
        Add a interface to the system
        :input interface:
        """
        self.interfaces.append(interface)

    def getInterfaces(self):
        """
        Returns an array with the interfaces for the system
        """
        return self.interfaces

    def __repr__(self):
        """
        Default print option for SystemInformation
        """
        return self.sysDescr

class Interface(object):
    def __init__(self, ifDescr, ifPhysAddress, network_mask):
        """
        Initialize a interface class
        :input ifDescr:
        :input ifPhysAddress:
        """
        self.ifDescr = ifDescr
        self.ifPhysAddress = ifPhysAddress
        self.network_mask = network_mask

    def __repr__(self):
        """
        Default print option for Interface
        """
        return self.ifDescr


import os
import subprocess
import xml.etree.ElementTree as ET

class CimParser(object):

    def __init__(self, wbemtarget):
        self.wbemtarget = wbemtarget

    def getSystemInformation(self):
        """
        Returns a SystemInformation object with associated Interface objects,
        each containing information gathered from the WBEM server
        """
        sysInfo = SystemInformation(self._getOperatingSystemData())
        interfaces = self._getIPInterfaces()
        for interface in interfaces:
            sysInfo.addInterface(Interface(interface[0], interface[1], interface[2]))

        return sysInfo

    def _execute(self, command):
        """
        Executes a shell command
        :input command:
        """
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        return err

    def _wbemRequest(self, operation, args):
        """
        Executes a wbemcli shell command with given arguments
        :input operation:
        :input args:
        """
        command = "wbemcli -dx -nl %s %s:%s" % (operation, self.wbemtarget, args)
        return self._execute(command)

    def _wbemResponseToXml(self, wbemResponse):
        """
        Extracts 'from server' XML from wbem response
        :input wbemResponse:
        """ 
        xmlStart = 'From server: <?xml version="1.0" encoding="utf-8" ?>'
        strings = wbemResponse.split(xmlStart)
        xml = '<?xml version="1.0" encoding="utf-8" ?>' + strings[1]
        return xml

    def _getIPInterfaces(self):
        """
        Returns a list of lists where each sublist represent one ip interface on the WBEM server.
        """
        args = "CIM_IPProtocolEndpoint"
        lists = self._getPropertyListsFromWBEM(args)
        interfaces = []
        for l in lists:
            interfaceInfo = self._getPropertyValues(l, ["Name", "IPv4Address", "SubnetMask"])
            interfaces.append(interfaceInfo)

        return interfaces

    def _getOperatingSystemData(self):
        """
        Returns the version string of the OperatingSystem object from the WBEM server
        """
        args = "CIM_OperatingSystem"
        lists = self._getPropertyListsFromWBEM(args)
        if len(lists) > 1:
            raise IndexError("Too many operative systems!")
        version = self._getPropertyValue(lists[0], "Version")
        return version


    def _getPropertyListsFromWBEM(self, args):
        """
        Returns a list of properties belonging to the CIM object given in args
        :input args:
        """
        lists = []
        wbemResponse = self._wbemRequest("ein", args)
        wbemXml = self._wbemResponseToXml(wbemResponse)
        instances = self._getInstancesFromXml(wbemXml)
        for instance in instances:
            keybinding = self._getKeyBindingsString(instance)
            instanceXml = self._getInstanceFromWBEM(keybinding)
            propertyList = self._getPropertyListFromXml(instanceXml)
            lists.append(propertyList)
        return lists

    def _getPropertyListFromXml(self, xml):
        """
        Returns a list of properties parsed from XML
        :input xml:
        """
        root = self._getXmlRoot(xml)
        propertyTree = root.findall("./MESSAGE/SIMPLERSP/IMETHODRESPONSE/IRETURNVALUE/INSTANCE/")
        return propertyTree

    def _getInstanceFromWBEM(self, key):
        """
        Returns the instance related to given key as XML
        :input key:
        """
        wbemResponse = self._wbemRequest("gi", key)
        return self._wbemResponseToXml(wbemResponse)

    def _getPropertyValue(self, propertyList, propertyName):
        """
        Returns the value of the property with given name from the given property list
        :input propertyList:
        :input propertyName:
        """
        for element in propertyList:
            if element.attrib['NAME'] == propertyName:
                return element.getchildren()[0].text

    def _getPropertyValues(self, propertyList, propertyNames):
        """
        Returns a list of property values given a list of property names from the given property list
        :input propertyList:
        :input propertyNames:
        """
        properties = []
        for name in propertyNames:
            properties.append(self._getPropertyValue(propertyList, name))
        return properties

    def _getInstancesFromXml(self, xml):
        """
        Returns a list of CIM object instances parsed from the given XML
        :input xml:
        """
        root = self._getXmlRoot(xml)
        instances = root.findall("./MESSAGE/SIMPLERSP/IMETHODRESPONSE/IRETURNVALUE/")
        return instances

    def _getKeyBindingsString(self, instance):
        """
        Returns a string with the key binding for the given CIM object instance
        :input instance:
        """
        keybinding = instance.attrib.values()[0] + "."
        for key in instance:
            keybinding += key.attrib.values()[0] + "="
            for child in key:
                keybinding += '"' + child.text + '"' + ","
        return "'" + keybinding.strip(',') + "'"


    def _getXmlRoot(self, xmlAsString):
        """
        Returns the root of the XML tree given as a string
        :input xmlAsString:
        """
        return ET.fromstring(xmlAsString)

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

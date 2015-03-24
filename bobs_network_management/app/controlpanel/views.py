from django.shortcuts import render
from bobs_network_management.app.snmp.snmp import SNMP
from bobs_network_management.app.cim.cim import CimParser

def controlpanel(request):
	"""
	Method called when the user enters Bobs network management site.
	"""
	return render(request, 'controlpanel/base.html',
		{"snmp_agents":getSNMPSystems(),
		"cim":getCIMSystems()})

def getSNMPSystems():
	"""
	Returns all SNMP systems in the network
	"""
	snmp = SNMP("ttm4128", "2c")
	snmp.work()
	return snmp.getSystems()

def getCIMSystems():
	"""
	Returns all CIM systems in the network
	"""
	cim = CimParser("http://ttm4128.item.ntnu.no:5988/root/cimv2")
	return cim.getSystemInformation()

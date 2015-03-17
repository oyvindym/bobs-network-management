from django.shortcuts import render
from bobs_network_management.app.snmp.snmp import SNMP
from bobs_network_management.app.cim.cim import CimParser

def controlpanel(request):
	snmp_agents = getSNMPSystems()
	cim = getCIMSystems()
	return render(request, 'controlpanel/base.html',
		{"snmp_agents":snmp_agents,
		"cim":cim})

def getSNMPSystems():
	snmp = SNMP("ttm4128", "2c")
	snmp.work()
	return snmp.getSystems()

def getCIMSystems():
	cim = CimParser("http://ttm4128.item.ntnu.no:5988/root/cimv2")
	return cim.getSystemInformation()

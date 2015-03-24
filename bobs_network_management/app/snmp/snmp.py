import subprocess

"""
IP addresses to the agents in Bobs network
"""
AGENTS = [
	'localhost',
	'129.241.209.2',
]

class SNMP(object):
	def __init__(self, community, version):
		"""
		Initialize the worker
		:input community: Community to listen on (ttm4128)
		:input version: SNMP version (2c)
		"""
		self.community = community
		self.version = version
		self.systems = []

	def execute(self, command, arguments):
		"""
		Execute the given command
		:input command:
		:input arguments:
		"""
		proc = subprocess.Popen(
				["%s -c %s -v %s %s %s" % (
					command,
					self.community,
					self.version,
					self.host,
					arguments)],
				stdout=subprocess.PIPE,
				shell=True)
		out, err = proc.communicate()
		return out

	def snmpget(self, arguments):
		"""
		Executes snmpget with the given arguments
		:input arguments:
		"""
		return self.execute("snmpget", arguments)

	def snmpwalk(self, arguments):
		"""
		Executes snmpwalk with the given arguments
		:input arguments:
		"""
		return self.execute("snmpwalk", arguments)

	def getIfDescr(self, i):
		"""
		Returns ifDescr for the ifDescr object with ID i
		:input i: ifDescr ID
		"""
		ifDescr = self.snmpget("ifDescr.%s" %(i))
		return ifDescr.split("STRING:")[-1].strip()

	def getSysDescr(self):
		"""
		Returns sysDescr
		"""
		sysDescr = self.snmpget("sysDescr.0")
		return sysDescr.split("STRING:")[-1].strip()

	def getIpAdEntNetMask(self, k):
		ipAdEntNetMask = self.snmpget("ipAdEntNetMask.%s" %(k))
		return ipAdEntNetMask.split("IpAddress:")[-1].strip()

	def getInterfaces(self, sys):
		"""
		Creates interfaces with the relevant information
		"""
		ips = self.getIps()
		for k in ips.keys():
			sys.addInterface(
					Interface(
						ipAdEntAddr=k,
						ipAdEntIfIndex=ips[k],
						ifDescr=self.getIfDescr(ips[k]),
						ipAdEntNetMask=self.getIpAdEntNetMask(k),		
					)
				)

	def setHost(self, host):
		"""
		Set remote host to use
		:input host:
		"""
		self.host = host

	def getIps(self):
		"""
		Returns a dictionary with interface IPs and the belonging interface index
		"""
		ips = {}
		for line in self.snmpwalk("ipAdEntIfIndex").split("\n"):
			if line:
				line = line.split("=")
				ip = line[0].strip().split("ipAdEntIfIndex.")[-1]
				index = int(line[-1].split("INTEGER:")[-1].strip())
				ips[ip] = index
		return ips

	def work(self):
		"""
		Work method for SNMP worker
		"""
		for agent in AGENTS:
			try:
				self.setHost(agent)
				sysDescr = self.getSysDescr()
				sys = SystemInformation(sysDescr)
				self.getInterfaces(sys)
				self.systems.append(sys)
			except:
				pass

	def getSystems(self):
		"""
		Returns the system with its interfaces
		"""
		return self.systems

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
	def __init__(self,
		ipAdEntAddr="",
		ipAdEntIfIndex="",
		ifDescr="",
		ipAdEntNetMask=""):
		"""
		Initialize a interface class
		:input ifDescr:
		:input ipAdEntAddr:
		:input ipAdEntNetMask:
		"""
		self.ipAdEntAddr = ipAdEntAddr
		self.ipAdEntIfIndex = ipAdEntIfIndex
		self.ifDescr = ifDescr
		self.ipAdEntNetMask = ipAdEntNetMask

	def __repr__(self):
		"""
		Default print option for Interface
		"""
		return self.ifDescr

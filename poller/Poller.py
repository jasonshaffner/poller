import re, easysnmp, subprocess
import iputils.IPUtils as IPUtils

#Generic poller, add any oid(s)
def poll(oids, host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	try: return _convertToDict(easysnmp.snmp_get(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
	except: return

#Generic bulk poller, add any oid(s)
def pollBulk(oids, host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	try: return _convertToDict(easysnmp.snmp_get_bulk(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
	except: return

#Base system poll, same as snmpbulkget system
def pollBase(host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return pollBulk('system', host, community, version=version, retries=retries, timeout=timeout)

def pollDescr(host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)

def pollContact(host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)

def pollName(host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)

def pollLocation(host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return poll('sysLocatino.0', host, community, version=version, retries=retries, timeout=timeout)

def pollInterfaceNumber(host, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)

def pollInterfaceIPs(host, community, index=None, v6=False, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	try: raw = easysnmp.snmp_walk('ipAddressIfIndex', hostname=host, version=version, community=community, retries=retries, timeout=timeout)
	except: return
	result = {}
	version = "2.16" if v6 else "1.4"
	for line in raw:
		if line.oid_index.startswith(version) and not line.oid_index.startswith(version + ".254"):
			addr = IPUtils.ipv6Reducer(":".join([str(format(int(digit), '02x')) for digit in line.oid_index.split('.')[2:]])) if v6 else str(line.oid_index.split('.', 2)[2])
			if index and int(line.value) == int(index): return {int(line.value):result}
			else: result.update({int(line.value):addr})
	return result

def pollInterfaceIP(host, community, interface, v6=False, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return pollInterfaces(host, community, v6=v6, version=version, retries=retries, timeout=timeout).get(interface)

def pollInterfaces(host, community, v6=False, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	if v6: address = "v6_address"
	else: address = "v4_address"
	ips = pollInterfaceIPs(host, community, v6=v6, version=version, retries=retries, timeout=timeout)
	result = []
	if ips:
		for ip in ips.keys():
			try: result.append({'interface':pollIfDescr(host, ip)['ifDescr'].split(' ')[0].strip(','), address:str(ips[ip])})
			except: continue
	return result

def pollInterfaceIndex(host, index, community, **kwargs):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return poll('ifIndex.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

def pollIfDescr(host, index):
	version = kwargs.get('version', 2)
	retries = kwargs.get('retries', 0)
	timeout = kwargs.get('timeout', 5)
	return poll('ifDescr.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

def pingPoll(iprange):
	return subprocess.run(['fping', '-ag', iprange, '-i', '10'], capture_output=True).stdout.decode().split('\n')

#Internal formatting function
def _convertToDict(easysnmpvariable):
	if type(easysnmpvariable) == easysnmp.variables.SNMPVariableList:
		output = {}
		for x in easysnmpvariable: output.update(convertToDict(x))
		return output
	else: return {str(easysnmpvariable.oid):str(easysnmpvariable.value)}

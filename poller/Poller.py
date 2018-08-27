import re, easysnmp, subprocess, time
import iputils.IPUtils as IPUtils

#Generic poller, add any oid(s)
async def async_poll(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    try:
        get = easysnmp.snmp_get(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
    except:
        return
    if get:
        return _convertToDict(get)

#Generic bulk poller, add any oid(s)
async def async_pollBulk(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    try:
        get = easysnmp.snmp_get_bulk(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
    except: return
    if get:
        return _convertToDict(get)

#Base system poll, same as snmpbulkget system
async def async_pollBase(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_pollBulk('system', host, community, version=version, retries=retries, timeout=timeout)

async def async_pollDescr(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_pollContact(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_pollName(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_pollLocation(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_poll('sysLocatino.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_pollInterfaceNumber(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_pollInterfaceIPs(host, community, index=None, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    try: raw = easysnmp.snmp_walk('ipAddressIfIndex', hostname=host, version=version, community=community, retries=retries, timeout=timeout)
    except: return
    result = {}
    version = "2.16" if v6 else "1.4"
    for line in raw:
        if line.oid_index.startswith(version) and not line.oid_index.startswith(version + ".254"):
            addr = IPUtils.reduce_ipv6_address(":".join([str(format(int(digit), '02x')) for digit in line.oid_index.split('.')[2:]])) if v6 else str(line.oid_index.split('.', 2)[2])
            if index and int(line.value) == int(index): return {int(line.value):result}
            else: result.update({int(line.value):addr})
    return result

async def async_pollInterfaceIP(host, community, interface, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_pollInterfaces(host, community, v6=v6, version=version, retries=retries, timeout=timeout).get(interface)

async def async_pollInterfaces(host, community, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    if v6: address = "v6_address"
    else: address = "v4_address"
    ips = await async_pollInterfaceIPs(host, community, v6=v6, version=version, retries=retries, timeout=timeout)
    result = []
    if ips:
        for ip in ips.keys():
            try:
                interface = await async_pollIfDescr(host, ip, community, version=version, retries=retries, timeout=timeout)
                result.append({'interface':interface['ifDescr'].split(' ')[0].strip(','), address:str(ips[ip])})
            except: continue
    return result

async def async_pollInterfaceIndex(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_poll('ifIndex.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

async def async_pollIfDescr(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 5)
    return await async_poll('ifDescr.' + str(index), host, community, version=version, retries=retries, timeout=timeout)


async def async_pingPoll(iprange):
    if re.search('/', iprange):
        return subprocess.run(['fping', '-ag', iprange, '-i', '10'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode().split('\n')
    raw = subprocess.Popen(['ping', "-i", "0.2", "-l", "3", "-w", "1", iprange], stdout=subprocess.PIPE)
    while raw.poll() == None: await asyncio.sleep(0.1)
    return False if raw.returncode else True

def pingPoll(iprange):
    if re.search('/', iprange):
        return subprocess.run(['fping', '-ag', iprange, '-i', '10'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode().split('\n')
    raw = subprocess.Popen(['ping', "-i", "0.2", "-l", "3", "-w", "1", iprange], stdout=subprocess.PIPE)
    while raw.poll() == None: time.sleep(0.1)
    return False if raw.returncode else True

#Internal formatting function
def _convertToDict(easysnmpvariable):
    if type(easysnmpvariable) == easysnmp.variables.SNMPVariableList:
        output = {}
        for x in easysnmpvariable: output.update(_convertToDict(x))
        return output
    else: return {str(easysnmpvariable.oid):str(easysnmpvariable.value)}

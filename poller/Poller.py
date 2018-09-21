import re
import easysnmp
import subprocess
import time
import asyncio
from functools import partial
import iputils.IPUtils as IPUtils

#Generic poller, add any oid(s)
def poll(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    try:
        get = easysnmp.snmp_get(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
    except:
        return
    if get:
        return _convertToDict(get)

@asyncio.coroutine
def async_poll(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    loop = asyncio.get_event_loop()
    try:
        get = yield from loop.run_in_executor(None, partial(easysnmp.snmp_get, oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
    except:
        return
    if get:
        return _convertToDict(get)

#Generic bulk poller, add any oid(s)
def poll_bulk(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    try:
        get = easysnmp.snmp_get_bulk(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
    except:
        return
    if get:
        return _convertToDict(get)

@asyncio.coroutine
def async_poll_bulk(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    loop = asyncio.get_event_loop()
    try:
        get = yield from loop.run_in_executor(None, partial(easysnmp.snmp_get_bulk, oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
    except:
        return
    if get:
        return _convertToDict(get)

#Base system poll, same as snmpbulkget system
def poll_base(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll_bulk('system', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_base(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll_bulk('system', host, community, version=version, retries=retries, timeout=timeout)

def poll_descr(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_descr(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_contact(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_contact(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_name(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_name(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_location(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll('sysLocatino.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_location(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysLocation.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_interface_number(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_interface_number(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_interface_ips(host, community, index=None, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
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

async def async_poll_interface_ips(host, community, index=None, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
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

def poll_interface_ip(host, community, interface, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll_interfaces(host, community, v6=v6, version=version, retries=retries, timeout=timeout).get(interface)

async def async_poll_interface_ip(host, community, interface, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll_interfaces(host, community, v6=v6, version=version, retries=retries, timeout=timeout).get(interface)

def poll_interfaces(host, community, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    if v6: address = "v6_address"
    else: address = "v4_address"
    ips = poll_interface_ips(host, community, v6=v6, version=version, retries=retries, timeout=timeout)
    result = []
    if ips:
        for ip in ips.keys():
            try:
                interface = poll_ifDescr(host, ip, community, version=version, retries=retries, timeout=timeout)
                result.append({'interface':interface['ifDescr'].split(' ')[0].strip(','), address:str(ips[ip])})
            except: continue
    return result

async def async_poll_interfaces(host, community, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    if v6: address = "v6_address"
    else: address = "v4_address"
    ips = await async_poll_interface_ips(host, community, v6=v6, version=version, retries=retries, timeout=timeout)
    result = []
    if ips:
        for ip in ips.keys():
            try:
                interface = await async_poll_ifDescr(host, ip, community, version=version, retries=retries, timeout=timeout)
                result.append({'interface':interface['ifDescr'].split(' ')[0].strip(','), address:str(ips[ip])})
            except:
                continue
    return result

def poll_interface_index(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll('ifIndex.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_interface_index(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('ifIndex.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

def poll_ifDescr(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return poll('ifDescr.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_ifDescr(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 0)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('ifDescr.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

def ping_poll(*iprange):
    if len(iprange) > 1:
        fping = subprocess.Popen(['fping', '-ag', iprange[0], iprange[1], '-i', '10'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return fping.communicate()[0].decode().split('\n')
    raw = subprocess.Popen(['ping', "-i", "0.2", "-l", "3", "-w", "1", iprange[0]], stdout=subprocess.PIPE)
    while raw.poll() == None:
        time.sleep(0.1)
    return False if raw.returncode else True

async def async_ping_poll(*iprange, retries=2):
    loop = asyncio.get_event_loop()
    asyncio.get_child_watcher().attach_loop(loop)
    if len(iprange) > 1:
        for attempt in range(retries):
            try:
                fping = await asyncio.create_subprocess_exec('fping', '-ag ', iprange[0], iprange[1], '-i', '10', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL, loop=loop)
                stdout, stderr = await fping.communicate()
                return stdout.decode().split('\n')
            except BlockingIOError:
                await asyncio.sleep(1)
    else:
        for attempt in range(retries):
            try:
                raw = await asyncio.create_subprocess_exec('ping', '-i', '0.2', '-l', '3', '-w', '1', iprange[0], stdout=asyncio.subprocess.PIPE, loop=loop)
                stdout, stderr = await raw.communicate()
                return False if raw.returncode else True
            except BlockingIOError:
                await asyncio.sleep(1)

#Internal formatting function
def _convertToDict(easysnmpvariable):
    if type(easysnmpvariable) == easysnmp.variables.SNMPVariableList:
        output = {}
        for x in easysnmpvariable:
            output.update(_convertToDict(x))
        return output
    else:
        return {str(easysnmpvariable.oid):str(easysnmpvariable.value)}

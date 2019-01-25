import re
import easysnmp
import subprocess
import time
import asyncio
from functools import partial
from poller.utils import IPUtils

#Generic poller, add any oid(s)
def poll(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
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
    retries = kwargs.get('retries', 1)
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
    retries = kwargs.get('retries', 1)
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
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    loop = asyncio.get_event_loop()
    try:
        get = yield from loop.run_in_executor(None, partial(easysnmp.snmp_get_bulk, oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
    except:
        return
    if get:
        return _convertToDict(get)

@asyncio.coroutine
def async_walk(oid, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    loop = asyncio.get_event_loop()
    try:
        get = yield from loop.run_in_executor(None, partial(easysnmp.snmp_walk, oid, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
    except:
        return
    if get:
        return _convertToDict(get)

def walk(oid, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    try:
        get = easysnmp.snmp_walk(oid, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
        print(get)
    except:
        return
    if get:
        return _convertToDict(get)

#Base system poll, same as snmpbulkget system
def poll_base(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll_bulk('system', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_base(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll_bulk('system', host, community, version=version, retries=retries, timeout=timeout)

def poll_descr(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_descr(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_contact(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_contact(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_name(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_name(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_location(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll('sysLocation.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_location(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('sysLocation.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_model(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    false_positives = re.compile("|".join(['MIDPLANE', \
                                            'NOSUCH', \
                                            'N/A', \
                                            'PORT', \
                                            'ÿ', \
                                            'DaughterCard', \
                                            'Switch\ Stack', \
                                            'Chassis\ System', \
                                            'Control Ethernet', \
                                            'NC6-RP', \
                                            '\d\d\d\-\d\d\d\d', \
                                            'Virtual', \
                                            '\d\d\.\d', \
                                            '\d\.\d\.\d', \
                                            '7600', \
                                            ]))
    model = False
    oids = [
            '1.3.6.1.2.1.47.1.1.1.1.13.4', \
            '1.3.6.1.2.1.47.1.1.1.1.13.1', \
            '1.3.6.1.2.1.47.1.1.1.1.2.1', \
            '1.3.6.1.2.1.47.1.1.1.1.2.149', \
            '1.3.6.1.2.1.47.1.1.1.1.13.1001', \
            '1.3.6.1.2.1.47.1.1.1.1.2.24555730', \
            '1.3.6.1.2.1.47.1.1.1.1.2.2', \
            '1.3.6.1.4.1.9.9.249.1.1.1.1.3', \
            '1.3.6.1.4.1.9.9.249.1.1.1.1.2', \
            '1.3.6.1.2.1.47.1.1.1.1.10.2', \
            '1.3.6.1.4.1.6527.3.1.2.2.1.6.1.2.2', \
            '1.3.6.1.4.1.6527.3.1.2.2.1.6.1.2.12', \
            '1.3.6.1.4.1.2636.3.40.1.4.1.1.1.8.0', \
            '1.3.6.1.4.1.2636.3.1.2.0', \
            ]
    while not model and oids:
        oid = oids.pop(0)
        model = poll(oid, host, community, version=version, retries=retries, timeout=timeout)
        if model:
            for value in model.values():
                if not value or not value.strip() or false_positives.search(value) or value == 'CHASSIS' or value == 'C ':
                    model = False
    return model

async def async_poll_model(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    false_positives = re.compile("|".join(['MIDPLANE', \
                                            'NOSUCH', \
                                            'N/A', \
                                            'PORT', \
                                            'ÿ', \
                                            'DaughterCard', \
                                            'Switch\ Stack', \
                                            'Chassis\ System', \
                                            'Control Ethernet', \
                                            'NC6-RP', \
                                            '\d\d\d\-\d\d\d\d', \
                                            'Virtual', \
                                            '\d\d\.\d', \
                                            '\d\.\d\.\d', \
                                            '7600', \
                                            ]))
    model = False
    oids = [
            '1.3.6.1.2.1.47.1.1.1.1.13.4', \
            '1.3.6.1.2.1.47.1.1.1.1.13.1', \
            '1.3.6.1.2.1.47.1.1.1.1.2.1', \
            '1.3.6.1.2.1.47.1.1.1.1.2.149', \
            '1.3.6.1.2.1.47.1.1.1.1.13.1001', \
            '1.3.6.1.2.1.47.1.1.1.1.2.24555730', \
            '1.3.6.1.2.1.47.1.1.1.1.2.2', \
            '1.3.6.1.4.1.9.9.249.1.1.1.1.3', \
            '1.3.6.1.4.1.9.9.249.1.1.1.1.2', \
            '1.3.6.1.2.1.47.1.1.1.1.10.2', \
            '1.3.6.1.4.1.6527.3.1.2.2.1.6.1.2.2', \
            '1.3.6.1.4.1.6527.3.1.2.2.1.6.1.2.12', \
            '1.3.6.1.4.1.2636.3.40.1.4.1.1.1.8.0', \
            '1.3.6.1.4.1.2636.3.1.2.0', \
            ]
    while not model and oids:
        oid = oids.pop(0)
        model = await async_poll(oid, host, community, version=version, retries=retries, timeout=timeout)
        if model:
            for value in model.values():
                if not value or not value.strip() or false_positives.search(value) or value == 'CHASSIS' or value == 'C ':
                    model = False
    return model

def poll_interface_number(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_interface_number(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)

def poll_interface_ips(host, community, index=None, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    result = {}
    raw = ''
    try:
        if not v6:
            raw = walk('ipAdEntIfIndex', host=host, version=version, community=community, retries=retries, timeout=timeout)
    except:
        pass
    if raw:
        for line in raw.keys():
            addr = ".".join(line.split('.')[-4:])
            index = int(raw.get(line))
            result.update({index:addr})
        if result:
            return result
    try:
        raw = walk('ipAddressIfIndex', host=host, version=version, community=community, retries=retries, timeout=timeout)
    except:
        return
    if raw:
        version = "2.16" if v6 else "1.4"
        for line in raw.keys():
            if int(raw.get(line)) and line.split('.', 1)[1].startswith(version) and not line.split('.', 1)[1].startswith(version + ".254"):
                addr = IPUtils.reduce_ipv6_address(":".join([str(format(int(digit), '02x')) for digit in line.split('.')[3:]])) if v6 else str(line.split('.', 3)[-1])
                if index and int(raw[line]) == int(index):
                    return {int(raw.get(line)):addr}
                else:
                    result.update({int(raw.get(line)):addr})
        if result:
            return result

async def async_poll_interface_ips(host, community, index=None, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    result = {}
    raw = ''
    try:
        if not v6:
            raw = await async_walk('ipAdEntIfIndex', host=host, version=version, community=community, retries=retries, timeout=timeout)
    except:
        pass
    if raw:
        for line in raw.keys():
            addr = ".".join(line.split('.')[-4:])
            index = int(raw.get(line))
            result.update({index:addr})
        if result:
            return result
    try:
        raw = await async_walk('ipAddressIfIndex', host=host, version=version, community=community, retries=retries, timeout=timeout)
    except:
        return
    if raw:
        version = "2.16" if v6 else "1.4"
        for line in raw.keys():
            if int(raw.get(line)) and line.split('.', 1)[1].startswith(version) and not line.split('.', 1)[1].startswith(version + ".254"):
                addr = IPUtils.reduce_ipv6_address(":".join([str(format(int(digit), '02x')) for digit in line.split('.')[3:]])) if v6 else str(line.split('.', 3)[-1])
                if index and int(raw[line]) == int(index):
                    return {int(raw.get(line)):addr}
                else:
                    result.update({int(raw.get(line)):addr})
        if result:
            return result

def poll_interface_ip(host, community, interface, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll_interfaces(host, community, v6=v6, version=version, retries=retries, timeout=timeout).get(interface)

async def async_poll_interface_ip(host, community, interface, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll_interfaces(host, community, v6=v6, version=version, retries=retries, timeout=timeout).get(interface)

def poll_ifOperStatus(host, community, index=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if index:
        raw = poll(".".join(('ifOperStatus', str(index))), host=host, version=version, community=community, retries=retries, timeout=timeout)
    else:
        try:
            return walk('ifOperStatus', host=host, version=version, community=community, retries=retries, timeout=timeout)
        except:
            return

async def async_poll_ifOperStatus(host, community, index=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if index:
        raw = await async_poll(".".join(('ifOperStatus', str(index))), host=host, version=version, community=community, retries=retries, timeout=timeout)
    else:
        try:
            return await async_walk('ifOperStatus', host=host, version=version, community=community, retries=retries, timeout=timeout)
        except:
            return

def poll_ifAdminStatus(host, community, index=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if index:
        raw = poll(".".join(('ifOperStatus', str(index))), host=host, version=version, community=community, retries=retries, timeout=timeout)
    else:
        try:
            return walk('ifAdminStatus', host=host, version=version, community=community, retries=retries, timeout=timeout)
        except:
            return

async def async_poll_ifAdminStatus(host, community, index=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if index:
        raw = await async_poll(".".join(('ifOperStatus', str(index))), host=host, version=version, community=community, retries=retries, timeout=timeout)
    else:
        try:
            return await async_walk('ifAdminStatus', host=host, version=version, community=community, retries=retries, timeout=timeout)
        except:
            return

def poll_interfaces(host, community, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if v6: address = "v6_address"
    else: address = "v4_address"
    ips = poll_interface_ips(host, community, v6=v6, version=version, retries=2, timeout=timeout)
    interfaces = poll_ifDescr(host, community, version=version, retries=2, timeout=timeout)
    oper = poll_ifOperStatus(host, community, version=version, retries=2, timeout=timeout)
    admin = poll_ifAdminStatus(host, community, version=version, retries=2, timeout=timeout)
    result = []
    if all((interfaces, oper, admin, ips)):
        for ip in ips.keys():
            if all((interfaces.get(".".join(('ifDescr', str(ip)))), oper.get(".".join(('ifOperStatus', str(ip)))), admin.get('.'.join(('ifAdminStatus', str(ip)))))):
                result.append({'interface':interfaces[".".join(('ifDescr', str(ip)))], address:str(ips[ip]),\
                        'oper_status':oper[".".join(('ifOperStatus', str(ip)))], 'admin_status':admin['.'.join(('ifAdminStatus', str(ip)))]})
    return result

async def async_poll_interfaces(host, community, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if v6: address = "v6_address"
    else: address = "v4_address"
    ips = await async_poll_interface_ips(host, community, v6=v6, version=version, retries=retries, timeout=timeout)
    interfaces = await async_poll_ifDescr(host, community, version=version, retries=retries, timeout=timeout)
    oper = await async_poll_ifOperStatus(host, community, version=version, retries=2, timeout=timeout)
    admin = await async_poll_ifAdminStatus(host, community, version=version, retries=2, timeout=timeout)
    result = []
    if all((interfaces, oper, admin, ips)):
        for ip in ips.keys():
            if all((interfaces.get(".".join(('ifDescr', str(ip)))), oper.get(".".join(('ifOperStatus', str(ip)))), admin.get('.'.join(('ifAdminStatus', str(ip)))))):
                result.append({'interface':interfaces[".".join(('ifDescr', str(ip)))], address:str(ips[ip]),\
                        'oper_status':oper[".".join(('ifOperStatus', str(ip)))], 'admin_status':admin['.'.join(('ifAdminStatus', str(ip)))]})
    return result

def poll_interface_index(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return poll('ifIndex.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_interface_index(host, index, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    return await async_poll('ifIndex.' + str(index), host, community, version=version, retries=retries, timeout=timeout)

def poll_ifDescr(host, community, index=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if index:
        return poll('ifDescr.' + str(index), host, community, version=version, retries=retries, timeout=timeout)
    else:
        return walk('ifDescr', host, community, version=version, retries=retries, timeout=timeout)

async def async_poll_ifDescr(host, community, index=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if index:
        return await async_poll('ifDescr.' + str(index), host, community, version=version, retries=retries, timeout=timeout)
    else:
        return await async_walk('ifDescr', host, community, version=version, retries=retries, timeout=timeout)

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
    if isinstance(easysnmpvariable, (easysnmp.variables.SNMPVariableList, list)):
        output = {}
        for x in easysnmpvariable:
            output.update(_convertToDict(x))
        return output
    else:
        if easysnmpvariable.oid_index:
            return {".".join((str(easysnmpvariable.oid), str(easysnmpvariable.oid_index))):str(easysnmpvariable.value)}
        else:
            return {str(easysnmpvariable.oid):str(easysnmpvariable.value)}

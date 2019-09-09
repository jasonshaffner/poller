import re
import json
import time
import logging
import asyncio
import pkgutil
import subprocess
from functools import partial

import easysnmp
from poller.utils import IPUtils

translations = json.loads(pkgutil.get_data('poller', 'translations'))

#Closures
def poll_func(oids, community, **kwargs):
    """
    Closure returning function that polls host using params provided at instantiation
    """
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    def poll(host):
        try:
            get = easysnmp.snmp_get(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
        except Exception as err:
            return
        if get:
            return _convertToDict(get)
    return poll

def async_poll_func(oids, community, **kwargs):
    """
    Closure returning function that asyncronously polls host using params provided at instantiation
    """
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)

    async def poll(host):
        loop = asyncio.get_event_loop()
        try:
            get = await loop.run_in_executor(None, partial(easysnmp.snmp_get, oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
        except Exception as err:
            return
        if get:
            return _convertToDict(get)
    return poll

#Generic poller, add any oid(s)
def poll(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    try:
        get = easysnmp.snmp_get(oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
    except Exception as err:
        return
    if get:
        return _convertToDict(get)

async def async_poll(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    loop = asyncio.get_event_loop()
    try:
        get = await loop.run_in_executor(None, partial(easysnmp.snmp_get, oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
    except Exception as err:
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
    except Exception as err:
        return
    if get:
        return _convertToDict(get)

async def async_poll_bulk(oids, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    loop = asyncio.get_event_loop()
    try:
        get = await loop.run_in_executor(None, partial(easysnmp.snmp_get_bulk, oids, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
    except Exception as err:
        return
    if get:
        return _convertToDict(get)

async def async_walk(oid, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    loop = asyncio.get_event_loop()
    try:
        get = await loop.run_in_executor(None, partial(easysnmp.snmp_walk, oid, hostname=host, version=version, community=community, retries=retries, timeout=timeout))
    except Exception as err:
        return
    if get:
        return _convertToDict(get)

def walk(oid, host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    try:
        get = easysnmp.snmp_walk(oid, hostname=host, version=version, community=community, retries=retries, timeout=timeout)
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
    poll_result = poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysDescr.0')

async def async_poll_descr(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = await async_poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysDescr.0')

def poll_contact(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysContact.0')

async def async_poll_contact(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = await async_poll('sysContact.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysContact.0')

def poll_name(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysName.0')

async def async_poll_name(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = await async_poll('sysName.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysName.0')

def poll_location(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = poll('sysLocation.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysLocation.0')

async def async_poll_location(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = await async_poll('sysLocation.0', host, community, version=version, retries=retries, timeout=timeout)
    if poll_result:
        return poll_result.get('sysLocation.0')

def poll_make_series_model(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    object_id = poll('sysObjectID.0', host, community, version=version, retries=retries, timeout=timeout)
    if not object_id:
        return
    oid = object_id.get('sysObjectID.0').lstrip('.')
    base = oid
    if not base:
        return
    oid_dict = {}
    while base and not oid_dict:
        oid_dict = translations.get(base)
        if not oid_dict:
            base = ".".join(base.split('.')[:-1])
    if not base or not oid_dict:
        return
    make = oid_dict.get('make')
    series = None
    model = None
    model_octets = re.sub(base, '', oid).split('.')[1:] if base != '1.3.6.1.4.1.2636.1.1.1' else re.sub(base, '', oid).split('.')[2:]
    if make == 'a10':
        if len(model_octets) == 1:
            series = oid_dict.get(model_octets[0]).get('series') if oid_dict.get(model_octets[0]) else None
        else:
            series = oid_dict.get(model_octets[0]).get(model_octets[1]).get('series') if oid_dict.get(model_octets[0]) and oid_dict.get(model_octets[0]).get(model_octets[1]) else None
        model_poll = poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)
        if not model_poll or not model_poll.get('sysDescr.0') or re.search('NOSUCHOBJECT', str(model_poll.values())):
            return
        a10_model_regex = re.compile(r'(?:AX|TH)\d{3,4}(?:S|-\d+)?')
        model = a10_model_regex.search(model_poll.get('sysDescr.0')).group(0) if a10_model_regex.search(model_poll.get('sysDescr.0')) else None
    elif make == 'arista':
        model = ''.join(oid_dict.get(octet) if oid_dict.get(octet) else octet for octet in model_octets)
        series = ''.join(oid_dict.get(octet) if oid_dict.get(octet) else octet for octet in model_octets[:2])
    elif make == 'cisco':
        model = oid_dict.get(model_octets[0]).get('model') if oid_dict.get(model_octets[0]) else None
        series = oid_dict.get(model_octets[0]).get('series') if oid_dict.get(model_octets[0]) else None
    elif make in ['alcatel', 'juniper', 'f5']:
        subset = oid_dict.get(model_octets[0])
        if subset:
            series = subset.get('series')
            if len(model_octets) == 1:
                model = subset.get('model') if subset.get('model') else subset.get('base')
            else:
                model = subset.get('model') if subset.get('model') else "".join((subset.get('base'), subset.get(model_octets[-1]).get('model')))
                if not series and make == 'juniper':
                    series = "".join((subset.get('base'), subset.get(model_octets[-1]).get('series')))
    elif make == 'avocent':
        poll_result = poll('1.3.6.1.4.1.10418.16.2.1.2.0', host, community, version=version, retries=retries, timeout=timeout)
        if poll_result and re.search('NOSUCHOBJECT', str(poll_result.values())):
            poll_result = None
        poll_result = poll('1.3.6.1.4.1.10418.26.2.1.2.0', host, community, version=version, retries=retries, timeout=timeout) if not poll_result else poll_result
        if poll_result and re.search(r'ACS\d{4}', str(poll_result.values())):
            model = re.search(r'ACS\d{4}', str(poll_result.values())).group(0)
            series = f'{model[:5]}00'
    elif make == 'niagara':
        poll_result = poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)
        if poll_result and poll_result.get('sysDescr.0') and not re.search('NOSUCHOBJECT', str(poll_result)):
            result = re.search('Model Number: (\w+)( |-)(\w+)', poll_result.get('sysDescr.0'), re.I)
            if result:
                if result.group(2) == ' ':
                    series = result.group(1)
                    model = result.group(3)
                else:
                    series = result.group(1)
                    model = "-".join((result.group(1), result.group(3)))
    if not all((make, series, model)):
        logging.debug(f'poll_make_series_model {host}: oid {oid} not fully recognized ({make}, {series}, {model}) ')
    return make, series, model

async def async_poll_make_series_model(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    object_id = await async_poll('sysObjectID.0', host, community, version=version, retries=retries, timeout=timeout)
    if not object_id:
        return None, None, None
    oid = object_id.get('sysObjectID.0').lstrip('.')
    base = oid
    if not base:
        return None, None, None
    oid_dict = {}
    while base and not oid_dict:
        oid_dict = translations.get(base)
        if not oid_dict:
            base = ".".join(base.split('.')[:-1])
    if not base or not oid_dict:
        return None, None, None
    make = oid_dict.get('make')
    series = None
    model = None
    model_octets = re.sub(base, '', oid).split('.')[1:] if base != '1.3.6.1.4.1.2636.1.1.1' else re.sub(base, '', oid).split('.')[2:]
    if make == 'a10':
        if len(model_octets) == 1:
            series = oid_dict.get(model_octets[0]).get('series') if oid_dict.get(model_octets[0]) else None
        else:
            series = oid_dict.get(model_octets[0]).get(model_octets[1]).get('series') if oid_dict.get(model_octets[0]) and oid_dict.get(model_octets[0]).get(model_octets[1]) else None
        model_poll = await async_poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)
        if not model_poll or not model_poll.get('sysDescr.0') or re.search('NOSUCHOBJECT', str(model_poll.values())):
            return None, None, None
        a10_model_regex = re.compile(r'(?:AX|TH)\d{3,4}(?:S|-\d+)?')
        model = a10_model_regex.search(model_poll.get('sysDescr.0')).group(0) if a10_model_regex.search(model_poll.get('sysDescr.0')) else None
    elif make == 'arista':
        model = ''.join(oid_dict.get(octet) if oid_dict.get(octet) else octet for octet in model_octets)
        series = ''.join(oid_dict.get(octet) if oid_dict.get(octet) else octet for octet in model_octets[:2])
    elif make == 'cisco':
        model = oid_dict.get(model_octets[0]).get('model') if oid_dict.get(model_octets[0]) else None
        series = oid_dict.get(model_octets[0]).get('series') if oid_dict.get(model_octets[0]) else None
    elif make in ['alcatel', 'juniper', 'f5']:
        subset = oid_dict.get(model_octets[0])
        if subset:
            series = subset.get('series')
            if len(model_octets) == 1:
                model = subset.get('model') if subset.get('model') else subset.get('base')
            else:
                model = subset.get('model') if subset.get('model') else "".join((subset.get('base'), subset.get(model_octets[-1]).get('model')))
                if not series and make == 'juniper':
                    series = "".join((subset.get('base'), subset.get(model_octets[-1]).get('series')))
    elif make == 'avocent':
        poll_result = await async_poll('1.3.6.1.4.1.10418.16.2.1.2.0', host, community, version=version, retries=retries, timeout=timeout)
        if poll_result and re.search('NOSUCHOBJECT', str(poll_result.values())):
            poll_result = None
        poll_result = await async_poll('1.3.6.1.4.1.10418.26.2.1.2.0', host, community, version=version, retries=retries, timeout=timeout) if not poll_result else poll_result
        if poll_result and re.search(r'ACS\d{4}', str(poll_result.values())):
            model = re.search(r'ACS\d{4}', str(poll_result.values())).group(0)
            series = f'{model[:5]}00'
    elif make == 'niagara':
        poll_result = poll('sysDescr.0', host, community, version=version, retries=retries, timeout=timeout)
        if poll_result and poll_result.get('sysDescr.0') and not re.search('NOSUCHOBJECT', str(poll_result)):
            result = re.search('Model Number: (\w+)( |-)(\w+)', poll_result.get('sysDescr.0'), re.I)
            if result:
                if result.group(2) == ' ':
                    series = result.group(1)
                    model = result.group(3)
                else:
                    series = result.group(1)
                    model = "-".join((result.group(1), result.group(3)))
    if not all((make, series, model)):
        logging.debug(f'poll_make_series_model {host}: oid {oid} not fully recognized ({make}, {series}, {model})')
    return make, series, model

def poll_interface_number(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)
    return poll_result.get('ifNumber.0')

async def async_poll_interface_number(host, community, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    poll_result = await async_poll('ifNumber.0', host, community, version=version, retries=retries, timeout=timeout)
    return poll_result.get('ifNumber.0')

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
    if v6: address = "v6_ip"
    else: address = "v4_ip"
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
    if v6: address = "v6_ip"
    else: address = "v4_ip"
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

def poll_ip_interfaces(host, community, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if v6: address = "v6_ip"
    else: address = "v4_ip"
    ips = poll_interface_ips(host, community, v6=v6, version=version, retries=2, timeout=timeout)
    interfaces = poll_ifDescr(host, community, version=version, retries=2, timeout=timeout)
    result = []
    if all((interfaces, ips)):
        for ip in ips.keys():
            if interfaces.get(".".join(('ifDescr', str(ip)))):
                result.append({interfaces[".".join(('ifDescr', str(ip)))]:str(ips[ip])})
    return result

async def async_poll_ip_interfaces(host, community, v6=False, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    if v6: address = "v6_ip"
    else: address = "v4_ip"
    ips = await async_poll_interface_ips(host, community, v6=v6, version=version, retries=2, timeout=timeout)
    interfaces = await async_poll_ifDescr(host, community, version=version, retries=2, timeout=timeout)
    result = []
    if all((interfaces, ips)):
        for ip in ips.keys():
            if interfaces.get(".".join(('ifDescr', str(ip)))):
                result.append({interfaces[".".join(('ifDescr', str(ip)))]:str(ips[ip])})
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

def poll_serial_number(host, community, index=None, make=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    oids = {'cisco': '.1.3.6.1.2.1.47.1.1.1.1.11',
            'juniper': '.1.3.6.1.4.1.2636.3.1.3',
            'f5': '.1.3.6.1.4.1.3375.2.1.3.3.3',
            'a10': '.1.3.6.1.4.1.22610.2.4.1.6.2',
            'avocent': '.1.3.6.1.4.1.10418.16.2.1.4',
            'alcatel': '.1.3.6.1.4.1.6527.3.1.2.2.1.8.1.5'}
    if make and oids.get(make):
        oids = {make: oids.get(make)}
    if index:
        for oid in oids.values():
            result = poll(oid + str(index), host, community, version=version, retries=retries, timeout=timeout)
            if result:
                return result
    else:
        for oid in oids.values():
            result = walk(oid, host, community, version=version, retries=retries, timeout=timeout)
            if result:
                return result

async def async_poll_serial_number(host, community, index=None, make=None, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    oids = {'cisco': '.1.3.6.1.2.1.47.1.1.1.1.11',
            'juniper': '.1.3.6.1.4.1.2636.3.1.3',
            'f5': '.1.3.6.1.4.1.3375.2.1.3.3.3',
            'a10': '.1.3.6.1.4.1.22610.2.4.1.6.2',
            'avocent': '.1.3.6.1.4.1.10418.16.2.1.4',
            'alcatel': '.1.3.6.1.4.1.6527.3.1.2.2.1.8.1.5'}
    if make and oids.get(make):
        oids = {make: oids.get(make)}
    if not isinstance(index, type(None)):
        for oid in oids.values():
            result = await async_poll(".".join((oid, str(index))), host, community, version=version, retries=retries, timeout=timeout)
            if result and 'NOSUCHOBJECT' not in result.values():
                return result
    else:
        for oid in oids.values():
            result = await async_walk(oid, host, community, version=version, retries=retries, timeout=timeout)
            if result:
                return result

def poll_number_of_chassis(host, community, make, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    oids = {'cisco': '.1.3.6.1.2.1.47.1.1.1.1.5',
            'alcatel': '.1.3.6.1.4.1.6527.3.1.2.2.1.8.1.8'}
    if make and oids.get(make):
        oid = oids.get(make)
    else:
        return
    snmp_output = walk(oid, host, community, version=version, retries=retries, timeout=timeout)
    if not snmp_output:
        logging.debug(f'No output from walk {host} {make} {oid}')
        return
    chassis = 0
    for key in snmp_output.keys():
        try:
            if make == 'cisco' and int(snmp_output.get(key)) == 3:
                chassis += 1
            elif make == 'alcatel' and re.search('chassis', snmp_output.get(key), flags=re.IGNORECASE):
                chassis += 1
        except ValueError as err:
            logging.debug(err)
    return chassis

async def async_poll_number_of_chassis(host, community, make, **kwargs):
    version = kwargs.get('version', 2)
    retries = kwargs.get('retries', 1)
    timeout = kwargs.get('timeout', 1)
    oids = {'cisco': '.1.3.6.1.2.1.47.1.1.1.1.5',
            'alcatel': '.1.3.6.1.4.1.6527.3.1.2.2.1.8.1.8'}
    if make and oids.get(make):
        oid = oids.get(make)
    else:
        return
    snmp_output = await async_walk(oid, host, community, version=version, retries=retries, timeout=timeout)
    if not snmp_output:
        logging.debug(f'No output from walk {host} {make} {oid}')
        return
    chassis = 0
    for key in snmp_output.keys():
        try:
            if make == 'cisco' and int(snmp_output.get(key)) == 3:
                chassis += 1
            elif make == 'alcatel' and re.search('chassis', snmp_output.get(key), flags=re.IGNORECASE):
                chassis += 1
        except ValueError as err:
            logging.debug(err)
    return chassis

def ping_poll(*iprange):
    if len(iprange) > 1:
        fping = subprocess.Popen(['fping', '-ag', iprange[0], iprange[1], '-i', '10'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return fping.communicate()[0].decode().split('\n')
    raw = subprocess.Popen(['ping', "-i", "0.2", "-l", "3", "-w", "1", iprange[0]], stdout=subprocess.PIPE)
    while raw.poll() == None:
        time.sleep(0.1)
    return False if raw.returncode else True

async def async_ping_poll(*iprange, retries=2):
    #Calling this function, make sure you have child watcher attached to loop
    loop = asyncio.get_event_loop()
    if len(iprange) > 1:
        for attempt in range(retries):
            try:
                fping = await asyncio.create_subprocess_exec('fping', '-ag', iprange[0], iprange[1], '-i', '10', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL, loop=loop)
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

#Helper formatting function
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

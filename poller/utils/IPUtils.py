import re

def reduce_ipv6_address(address):
    """
    Converts to IPV6 address from snmp poll notation: XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX
    """
    ipv6_add = ''
    while len(address) > 0:
        prefix = "".join(address.split(":")[:2])
        address = ":".join(address.split(":")[2:])
        while prefix.startswith('0') and len(prefix) > 1:
            prefix = prefix[1:]
        ipv6_add = ":".join([ipv6_add, prefix]) if ipv6_add else prefix
    zeroes = [i for i, x in enumerate(ipv6_add.split(":")) if x == "0"]
    if not zeroes:
        return ipv6_add
    index = 0
    current = 0
    longest = 0
    current_streak = []
    longest_streak = []
    streaking = True
    while index < len(zeroes):
        if (index == 0 and zeroes[1:] and zeroes[1] - 1 == zeroes[0]) \
            or (current == 0 and zeroes[index + 1:] and zeroes[index + 1] - 1 == zeroes[index]) \
            or (zeroes[index] - 1 == zeroes[index - 1]):
            current += 1
            current_streak.append(zeroes[index])
            if current > longest:
                longest = current
                longest_streak = current_streak[:]
        else:
            current = 0
            current_streak = []
        index += 1
    longest_streak = set(longest_streak)
    index = 0
    ipv6_address = ''
    double_colon = ":"
    right = ":" if 7 in longest_streak else ""
    while index < len(ipv6_add.split(":")):
        if index in longest_streak:
            ipv6_address += double_colon
            double_colon = ""
        else:
            ipv6_address += ":" + ipv6_add.split(":")[index] if ipv6_address else ipv6_add.split(":")[index]
        index += 1
    return ipv6_address + right

def validate_ipv4_address(address):
    """
    Validates IPv4 Addresses
    """
    return all(re.match('\.|\d', c) for c in address) \
        and address.count('.') == 3 \
        and all(re.match(r'\d{1,3}', d) for d in address.split('.')) \
        and all(0 <= int(d) <= 255 for d in address.split('.'))

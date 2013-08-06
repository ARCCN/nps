
def get_next_IP(IP):
    '''Generate next IP address. The next IP address is the incrementation (+1) of current IP address.

    Args:
        IP: The current IP address.

    Returns:
        The next incremented IP address. The input and output IP addresses are strings.

    '''
    octets = IP.split('.')
    if int(octets[3]) + 1 >= 255:
        next_IP = octets[0] + '.' + octets[1] + '.' + str(int(octets[2]) + 1) + '.' + '1'
    else:
        next_IP = octets[0] + '.' + octets[1] + '.' + octets[2] + '.' + str(int(octets[3]) + 1)
    return next_IP


def get_next_IP_pool(IP, hosts_number):
    '''Generate the first IP address on next IP address pool. Depends on IP address pool size.

    Args:
        IP: The first address of current pool.
        hosts_number: The size of current pool.

    Returns:
        The first IP address of the next pool. The input and output IP addresses are strings.
    '''
    octets = IP.split('.')
    if int(octets[3]) + hosts_number >= 255:
        new_oct = divmod(int(octets[3]) + hosts_number, 255)
        next_IP_pool = octets[0] + '.' + octets[1] + '.' + str(int(octets[2]) + int(new_oct[0])) \
                       + '.' + str(int(new_oct[1]) + int(new_oct[0]))
    else:
        next_IP_pool = octets[0] + '.' + octets[1] + '.' + str(int(octets[2])) \
                       + '.' + str(int(octets[3]) + hosts_number)
    return next_IP_pool

def get_next_host_name(host):
    '''Generate the next host name in Mininet network. he next host name is the incremention (+1)
        of current host name.

    Args:
        host: The current host name.

    Returns:
        The next host incremented name.
    '''
    next_nost = 'h' + str(int(host[1:]) + 1)
    return next_nost


def get_random_IP():
    '''Generated random IP address.

    Returns:
        The random IP address.
    '''
    IP = str(randint(1,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255))
    return IP


def get_random_test_IP():
    '''Generated random IP address.

    Returns:
        The random IP address.
    In this test function is a smaller pool of possible IP addresses. Used for experiments with malware
    propagation.
    '''
    IP = str(randint(1,1)) + '.' + str(randint(1,2)) + '.' + str(randint(1,254)) + '.' + str(randint(1,254))
    return IP


def randomize_infected(prob):
    '''Make decision of host infection, depends on infection probability.

    Args:
        prob: Host infection probability.

    Returns:
        True: If the host is infected.
        False: If the host is NOT infected.
    '''
    r = randint(1,100)
    if r <= prob:
        return True
    else:
        return False
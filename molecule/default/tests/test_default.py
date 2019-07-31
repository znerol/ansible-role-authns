import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_SOA(host):
    host_vars = host.ansible.get_variables()
    hostname = host_vars["inventory_hostname"]

    zone = '.'.join(hostname.split('.')[1:])

    host.run_expect([0], "/usr/bin/nslookup -type=SOA %s. localhost", zone)


def test_TXT(host):
    host_vars = host.ansible.get_variables()
    hostname = host_vars["inventory_hostname"]

    zone = '.'.join(hostname.split('.')[1:])

    host.run_expect([0], "/usr/bin/nslookup -type=TXT _test.%s. localhost",
                    zone)


def test_refuse_recurse(host):
    host.run_expect([1], "/usr/bin/nslookup -type=SOA com. localhost")


def test_ddns(host):
    host_vars = host.ansible.get_variables()
    hostname = host_vars["inventory_hostname"]

    zone = '.'.join(hostname.split('.')[1:])

    host.run_expect([0],
                    "/usr/bin/nsupdate -k ~/files/key.%s ~/files/nsupdate.%s",
                    hostname, hostname)

    host.run_expect([0], "/usr/bin/nslookup -type=TXT _test-2.%s. localhost",
                    zone)

Role Name
=========

[![Build Status](https://travis-ci.org/znerol/ansible-role-authns.svg?branch=master)](https://travis-ci.org/znerol/ansible-role-authns)

BIND Authoritative Name Server

Requirements
------------

None.

Role Variables
--------------

This role contains multiple `task` files. The `main` task file only imports
some of them:

1. [bind-install.yml](#variables-for-bind-installyml): Installs required
   packages on the system.
1. [bind-config.yml](#variables-for-bind-configyml): Prepares a minimal
   configuration for a non-recursive authoritative-only DNS server.
1. [bind-service.yml](#variables-for-bind-serviceyml): Sets up the bind
   service.

The following task files contain steps used to setup zones / resource records
and ddns update keys.

1. [zone.yml](#variables-for-zoneyml): Setup DNS zones with SOA and NS records
   and an initial set of resource records (rr).
1. [key.yml](#variables-for-keyyml): Setup a key for dynamic DNS updates.


### Variables for bind-install.yml

None.

### Variables for bind-config.yml

Variables in this section should be left to their defaults in most cases.

```
authns_main_config_owner: root
authns_main_config_group: root
authns_main_config_mode: 0644
authns_main_config_selevel: # omitted by default
authns_main_config_serole: # omitted by default
authns_main_config_setype: # omitted by default
authns_main_config_seuser: # omitted by default

authns_local_config_file: "{{ authns_bind_etc_path }}/named.conf.local"
authns_local_config_owner: root
authns_local_config_group: root
authns_local_config_mode: 0644
authns_local_config_selevel: # omitted by default
authns_local_config_serole: # omitted by default
authns_local_config_setype: # omitted by default
authns_local_config_seuser: # omitted by default

authns_options_config_file: "{{ authns_bind_etc_path }}/named.conf.options"
authns_options_config_owner: root
authns_options_config_group: root
authns_options_config_mode: 0644
authns_options_config_selevel: # omitted by default
authns_options_config_serole: # omitted by default
authns_options_config_setype: # omitted by default
authns_options_config_seuser: # omitted by default
```

### Variables for bind-service.yml

None.

### Variables for zone.yml

The following variables are *required* when importing the `zone` task file:

* Either one of `authns_zone_rr_content` or `authns_zone_rr_src` must be
  defined. Use the former to supply the content of a zone file directly and the
  later to specify a file containing the records. Those variables are
  referenced from a call to [copy][Ansible-Copy] module, hence docs apply here
  as well. Note: It is completely valid to set `authns_zone_rr_content` to the
  empty string.

When setting up a new zone, the following variables are optional:

* `authns_zone_name`: The zone domain name. Defaults to the domain of inventory
  hostname.
* `authns_zone_allow_update`: A list of ACL rules defining which IP/key
  combination is allowed to update the zone dynamically. Use the predefined
  variable `{{ authns_acl_require_localnets_and_update_key }}` for the slightly
  confusing ACL which allows dynamic updates to succeed only if the UPDATE
  request comes from an address in localnets, and if it is signed using the key
  from the `authns_update_key_name` variable. See [TSIG-Based Access
  Control][ARM-TSIG] in the Bind9 Administrator Reference Manual.
* `authns_zone_db_ns`: Used for the `NS` record in the zone, defaults to the
  inventory hostname.
* `authns_zone_db_ns_ip4` and `authns_zone_db_ns_ip6`: Used for `A` and `AAAA`
  records for the zones nameserver. Default to the ip of inventory hostname if
  its domain matches `authns_zone_name`.
* If `authns_zone_dnssec` is set to `true`, a directory is created with the
  correct access mode and DNSSEC configuration is added to the zone config.
  Note that this does *not* generate any DNSSEC keys.

The remaining variables in this section should be left to their defaults in
most cases.

```
authns_zone_name: "{{ inventory_hostname.split('.')[1:]|join('.') }}"
authns_zone_allow_update: []

authns_zone_dnssec: false
authns_zone_dnssec_key_name: "{{ authns_zone_name }}"
authns_zone_dnssec_key_dir: "{{ authns_bind_etc_path }}/dnssec.{{ authns_dnssec_key_name }}"
authns_zone_dnssec_key_owner: root
authns_zone_dnssec_key_group: "{{ authns_os_bind_group }}"
authns_zone_dnssec_key_mode: 0750
authns_zone_dnssec_key_selevel: # omitted by default
authns_zone_dnssec_key_serole: # omitted by default
authns_zone_dnssec_key_setype: # omitted by default
authns_zone_dnssec_key_seuser: # omitted by default

authns_zone_config_file: "{{ authns_bind_etc_path }}/zones.{{ authns_zone_name }}"
authns_zone_config_owner: root
authns_zone_config_group: root
authns_zone_config_mode: 0644
authns_zone_config_selevel: # omitted by default
authns_zone_config_serole: # omitted by default
authns_zone_config_setype: # omitted by default
authns_zone_config_seuser: # omitted by default
```

```
authns_zone_db_file: "{{ authns_bind_db_path }}/db.{{ authns_zone_name }}"
authns_zone_db_owner: root
authns_zone_db_group: root
authns_zone_db_mode: 0644
authns_zone_db_selevel: # omitted by default
authns_zone_db_serole: # omitted by default
authns_zone_db_setype: # omitted by default
authns_zone_db_seuser: # omitted by default

authns_zone_db_ns: "{{ inventory_hostname }}"
authns_zone_db_hostmaster: "hostmaster.{{ authns_zone_name }}"
authns_zone_db_serial: 1
authns_zone_db_ttl: 21600
authns_zone_db_refresh: 1800
authns_zone_db_retry: 900
authns_zone_db_expire: 604800
authns_zone_db_minimum: 1200

authns_zone_db_ns_in_zone: "{{ authns_zone_db_ns == authns_zone_name or authns_zone_db_ns.endswith('.{:s}'.format(authns_zone_name)) | bool }}"
authns_zone_db_ns_ip4: "{{ ansible_default_ipv4['address'] | default('') }}"
authns_zone_db_ns_ip6: "{{ ansible_default_ipv6['address'] | default('') }}"
```

```
authns_zone_rr_file: "{{ authns_zone_db_file }}.rr"
authns_zone_rr_owner: root
authns_zone_rr_group: root
authns_zone_rr_mode: 0644

authns_zone_rr_selevel: # omitted by default
authns_zone_rr_serole: # omitted by default
authns_zone_rr_setype: # omitted by default
authns_zone_rr_seuser: # omitted by default

authns_zone_rr_checksum: # omitted by default
authns_zone_rr_content: # omitted by default
authns_zone_rr_decrypt: # omitted by default
authns_zone_rr_follow: # omitted by default
authns_zone_rr_force: # omitted by default
authns_zone_rr_local_follow: # omitted by default
authns_zone_rr_remote_src: # omitted by default
authns_zone_rr_src: # omitted by default
```

### Variables for key.yml

The following variables are *required* when importing the `key` task file:

* Either one of `authns_update_key_content` or `authns_update_key_src` must be
  defined. Use the former to supply a ddns update key directly and the later to
  specify a file containing the it. Those variables are referenced from a call
  to [copy][Ansible-Copy] module, hence docs apply here as well. Use
  `ddns-confgen -q -k {{ authns_update_key_name }}` to generate a ddns key.

When setting up a new zone, the following variables are optional:

* `authns_update_key_name`: The zone domain name. Defaults to the inventory
  hostname.

The remaining variables in this section should be left to their defaults in
most cases.

```
authns_update_key_name: "{{ inventory_hostname }}"

authns_update_key_file: "{{ authns_bind_etc_path }}/key.{{ authns_update_key_name }}"
authns_update_key_owner: root
authns_update_key_group: "{{ authns_os_bind_group }}"
authns_update_key_mode: 0640

authns_update_key_selevel: # omitted by default
authns_update_key_serole: # omitted by default
authns_update_key_setype: # omitted by default
authns_update_key_seuser: # omitted by default

authns_update_key_checksum: # omitted by default
authns_update_key_content: # omitted by default
authns_update_key_decrypt: # omitted by default
authns_update_key_follow: # omitted by default
authns_update_key_force: # omitted by default
authns_update_key_local_follow: # omitted by default
authns_update_key_remote_src: # omitted by default
authns_update_key_src: # omitted by default
```




Dependencies
------------

None.

Example Playbook
----------------

    - hosts: all
      vars:
        authns_zone_rr_content: |
          _test 1D IN TXT "test rr"
        authns_update_key_content: |
          key "{{ inventory_hostname }}" {
              algorithm hmac-sha256;
              secret "{{ my_secret_update_key_variable }}";
          };
      tasks:
        - import_role:
            name: znerol.authns

        - import_role:
            name: znerol.authns
            tasks_from: zone

        - import_role:
            name: znerol.authns
            tasks_from: key

        - import_role:
            name: znerol.authns
            tasks_from: utilities

License
-------

BSD


[ARM-TSIG]: https://ftp.isc.org/isc/bind9/cur/9.11/doc/arm/Bv9ARM.ch04.html#id-1.5.6.8
[Ansible-Copy]: https://docs.ansible.com/ansible/latest/modules/copy_module.html

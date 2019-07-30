Role Name
=========

[![Build Status](https://travis-ci.org/znerol/ansible-role-authns.svg?branch=master)](https://travis-ci.org/znerol/ansible-role-authns)

BIND Authoritative Name Server

Requirements
------------

None.

Role Variables
--------------



Dependencies
------------

None.

Example Playbook
----------------

    - hosts: all
      vars:
        authns_zone_rr_content: |
          _test 1D IN TXT "test rr"
      tasks:
        - import_role:
            name: znerol.authns

        - import_role:
            name: znerol.authns
            tasks_from: zone

        - import_role:
            name: znerol.authns
            tasks_from: utilities

License
-------

BSD

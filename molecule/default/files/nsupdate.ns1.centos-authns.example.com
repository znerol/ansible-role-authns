server localhost
add _test-2.centos-authns.example.com. 3600 IN TXT "other test rr"
send

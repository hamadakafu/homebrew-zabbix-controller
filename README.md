# Zabbix CLI

## Example
### Valid Command
`zabbix_controller -u username -p password hosts list`
`zabbix_controller -u username -p password hosts -m name:^server$ list`
### Invalid Command
`zabbix_controller hosts -u username -p password list`
`zabbix_controller -u username -p password hosts list -m name:^server$ `

## Command 
### zabbixctl [options] command ...
#### Options
These options are only set at `zabbixctl [options] command ...`.
`zabbixctl command [options] ...` is not accepted.
##### --help
```bash
zabbixctl --help
```
##### --apiserver-address, -aa
```bash
zabbixctl -aa http://localhost:8081
```
##### --username, -u, --password, -p
Used for zabbix login
```bash
zabbixctl --username Admin --password zabbix_password
```
##### --basicauth_username, -bu, --basicauth_password, -bp
Used for basic authentication
```bash
zabbixctl -bu alis -bp alis_password
```
##### --dry-run
If you set `--dry-run`, only get API is executed, then ZabbixCTL state is printed.
Create, update, delete API is not executed.
```bash
zabbixctl --dry-run
```

### zabbixctl host [options] ...
#### Options

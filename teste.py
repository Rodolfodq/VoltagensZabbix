from zabbix_api import ZabbixAPI
from credentials import user, password
import pprint

zapi = ZabbixAPI(server="http://172.16.10.133/zabbix")
zapi.login(user, password)
# id_grupo = zapi.hostgroup.get({"filter": {"name": ['COOPERCITRUS-MON-ENERGIA']}})
# print(id_grupo)
hosts = zapi.host.get({"groupids": 1020})
#pprint.pprint(hosts)
template = zapi.item.get({"hostids": 22593})
pprint.pprint(template)

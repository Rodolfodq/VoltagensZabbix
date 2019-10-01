from zabbix_api import ZabbixAPI
from credentials import user, password, endereco

zapi = ZabbixAPI(server=endereco)
zapi.login(user, password)


def get_id_hosts(grupos):
    host_ids = {}
    for id in grupos:
        hosts = zapi.host.get({"groupids": [id], "monitored_hosts": 1})
        for i in range(len(hosts)):
            if hosts[i]['hostid'] not in host_ids:
                host_ids[hosts[i]['hostid']] = hosts[i]['host']
            else:
                pass
    return host_ids


def get_template(host_ids):
    volt_dict = {}
    for j in host_ids:
        template = zapi.item.get({"hostids": j})
        voltagem = ''
        ent_voltagem = ''
        try:
            for y in range(len(template)):
                voltagem = template[y]['lastvalue']
                ent_voltagem = template[y + 1]['lastvalue']
                if template[y]['key_'] == 'snmp.volt.voltagembateria' or \
                        template[y]['key_'] == 'snmp.volt.bateria' or \
                        template[y]['key_'] == 'snmp.volt.netprobe.voltagem' or \
                        template[y]['name'] == 'Tensão da Bateria':
                    break

            volt_dict[j] = host_ids[j], voltagem, ent_voltagem
        except:
            print('Erro! Dados não coletados.\nHost: {}'.format(host_ids[j]))
    return volt_dict

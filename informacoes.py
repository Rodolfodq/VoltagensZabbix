from zabbix_api import ZabbixAPI
from credentials import user, password, endereco
import datetime

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
    print('Inicio da coleta de dados: {}'.format(datetime.datetime.now().time().strftime('%H:%M:%S')))
    volt_dict = {}
    for j in host_ids:
        template = zapi.item.get({"hostids": j})
        voltagem = ''
        ent_voltagem = ''
        status_rede = ''
        try:
            for y in range(len(template)):
                if template[y]['key_'] == 'snmp.volt.voltagembateria' or \
                        template[y]['key_'] == 'snmp.volt.bateria' or \
                        template[y]['key_'] == 'snmp.volt.netprobe.voltagem' or \
                        template[y]['name'] == 'Tensão da Bateria':
                    voltagem = template[y]['lastvalue']
                    ent_voltagem = template[y + 1]['lastvalue']
                    for x in range(len(template)):
                        if template[x]['name'] == 'Status da Bateria' or \
                                template[x]['key_'] == 'snmp.volt.mododeoperacao':
                            status_rede = template[x]['lastvalue']
                    break

            volt_dict[j] = host_ids[j], voltagem, ent_voltagem, status_rede
        except Exception as erro:
            print('Erro! Dados não coletados.\nHost: {}\nErro: {}'.format(host_ids[j], str(erro)))
    print('Fim da coleta de dados: {}'.format(datetime.datetime.now().time().strftime('%H:%M:%S')))
    return volt_dict

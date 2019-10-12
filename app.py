from informacoes import get_id_hosts, get_template
from manipula_dados import salva_txt, open_txt, compara_valores, get_grupos
import time

while True:
    id_grupo = get_grupos()
    grupos = {}
    for i in range(len(id_grupo)):
        grupos[id_grupo[i]['groupid']] = id_grupo[i]['name']

    host_ids = get_id_hosts(grupos)
    volt_dict = get_template(host_ids)
    dados_antigos = open_txt()  # guarda na variável os valores da consulta anterior
    compara_valores(dados_antigos, volt_dict)  # compara os valores da consulta anterior com a atual
    salva_txt(volt_dict)  # salva no txt os valores da consulta atual
    time.sleep(3600)

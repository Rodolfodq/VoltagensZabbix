import ast
from send_alerta import send_text
from zabbix_api import ZabbixAPI
from credentials import user, password, endereco

zapi = ZabbixAPI(server=endereco)
zapi.login(user, password)


def get_grupos():
    id_grupo = zapi.hostgroup.get({"filter": {"name": ['FONTE 24V', 'FONTE 48V',
                                                       'SISTEMA SOLAR', 'COOPERCITRUS-MON-ENERGIA']}})
    return id_grupo


def open_txt():
    with open("Valores/Voltagens.txt", 'r', encoding="utf8") as dados:
        arq = dados.read()
    data = ast.literal_eval(arq)
    return data


def compara_valores(dados_antigos, volt_dict):
    fase = 0
    for i in volt_dict:
        if i in dados_antigos:
            diferenca = (float(dados_antigos[i][1])) - (float(volt_dict[i][1]))
            if diferenca >= 0.1:
                text = ('{}\nAtual: {:.2f}V\nAntigo: {:.2f}V'
                        .format(volt_dict[i][0], float(volt_dict[i][1]), float(dados_antigos[i][1])))
                textemail = ('Foi identificada uma queda de {:.2f}V no(a) {} no periodo de 1 hora.\n'
                             'Favor encaminhar este chamado para análise N2.'.format(diferenca, volt_dict[i][0]))
                #send_text(text)
                #send_text(textemail)
                print(textemail)
                print(text)
                fase = fase + 1
            else:
                pass
        else:
            print('Não encontrado: {}'.format(volt_dict[i][0]))
    print('Comparações finalizadas.')
    if fase == 0:
        text = 'Não foi identificada nenhuma diferença maior que 5V no intervalo de 1 hora'
        print(text)
        send_text(text)
    else:
        pass
    return


def salva_txt(volt_dict):
    try:
        with open("Valores/Voltagens.txt", 'w', encoding="utf8") as info:
            info.write(str(volt_dict))
        print("Arquivo salvo com suceso.")
        return
    except:
        print('Falha ao salvar arquivo. Verifique a permissão de escrita.')
        return

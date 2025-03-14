# LÓGICAS

from methods import *
from models import *
import json  # Certifique-se de importar json
from os import *
import time


def process_custom_attributes():
    apikey = "429683C4C977415CAAFCCE10F7D57E11"
    
    print("Obtendo atributos personalizados...")
    attributes = get_custom_attributes()
    print("Atributos recebidos:", attributes)
    
    # Verifica se os atributos são um dicionário e converte para JSON
    if isinstance(attributes, dict):
        attributes = json.dumps(attributes)
        print("Atributos convertidos para JSON:", attributes)

    # Processa o resultado com extract_jid
    remote_jid = extract_jid(attributes)
    print("JID extraído:", remote_jid)

     # Verifica e atualiza o arquivo jid.temp
    new_jids = update_jid_file(remote_jid)
    print("Novos JIDs processados:", new_jids)

    # Obtém os JIDs removidos
    removed_jids = get_removed_jids(remote_jid)
    print("JIDs removidos:", removed_jids)
    
    # Altera o status dos JIDs removidos, se houver
    if removed_jids:
        change_status(apikey, removed_jids)
        print("Status atualizado para JIDs removidos.")
    else:
        print("Nenhum JID removido para processar.")



if __name__ == "__main__":
      while True:
        process_custom_attributes()
        print("Aguardando 20 segundos para a próxima execução...")
        time.sleep(20)  # Pausa de 20 segundos (20 segundos) antes da próxima execução



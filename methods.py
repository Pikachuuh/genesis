#COLOCAR TODAS AS FUNÇÕES

import requests
import json
import re
import os

def extract_jid(json_string):
    """Extrai todos os JIDs do JSON retornado pelo banco de dados."""
    try:
        lines = [line.strip() for line in json_string.strip().split("\n") if line.strip()]
        data = [json.loads(line) for line in lines if line.startswith("{") and line.endswith("}")]
        return [item.get("jid", "") for item in data if "jid" in item]
    except json.JSONDecodeError:
        return re.findall(r'"jid"\s*:\s*"([^"]+)"', json_string)

def check_and_read_jid_file(filename="jid.temp"):
    """Verifica e lê o arquivo 'jid.temp'. Se não existir, cria um com uma lista vazia."""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao ler o arquivo {filename}: {e}")
            return []
    else:
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump([], file)
            return []
        except IOError as e:
            print(f"Erro ao criar o arquivo {filename}: {e}")
            return []

def update_jid_file(remote_jids, filename="jid.temp"):
    """Compara a lista de remote_jid com o arquivo jid.temp e adiciona os novos itens."""
    
    existing_jids = check_and_read_jid_file(filename)
    new_jids = [jid for jid in remote_jids if jid not in existing_jids]

    if new_jids:
        updated_jids = existing_jids + new_jids
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(updated_jids, file, indent=4)
            print(f"Novos JIDs adicionados ao {filename}: {new_jids}")
        except IOError as e:
            print(f"Erro ao escrever no arquivo {filename}: {e}")
    else:
        print("Nenhum novo JID para adicionar.")

    return new_jids  

def get_removed_jids(remote_jids, filename="jid.temp"):
    """Compara a lista salva com a lista remota e retorna os JIDs que foram removidos."""
    
    existing_jids = check_and_read_jid_file(filename)
    removed_jids = [jid for jid in existing_jids if jid not in remote_jids]

    return removed_jids  # Retorna os JIDs removidos

def change_status(apikey, removed_jids):
    """Envia requisições para alterar o status de cada JID removido."""
    url = "http://suaurl/typebot/changeStatus/TYPEBOT"
    headers = {"apikey": apikey, "Content-Type": "application/json"}

    for jid in removed_jids:
        body = {"remoteJid": jid, "status": "closed"}

        try:
            response = requests.post(url, json=body, headers=headers, timeout=10)
            response.raise_for_status()
            print(f"Status alterado para {jid}: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao alterar status de {jid}: {e}")

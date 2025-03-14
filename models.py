#TODA INTERAÇÃO COM O BANCO


import subprocess


def get_custom_attributes():
    command = [
        "sudo", "docker", "exec", "chatwoot_postgres_1",
        "psql", "-U", "postgres", "-d", "chatwoot", #"-t", "-A", "-F", ",",
        "-c", "SELECT custom_attributes FROM conversations WHERE status = 0;"   
     ]


    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Saída do comando:", result.stdout)  # Debug
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando:", str(e))
        return {"error": str(e)}

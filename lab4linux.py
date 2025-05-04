import paramiko
import random
import string
import json
import re

# SSH prisijungimo nustatymai
SSH_HOST = "172.20.10.2"  
SSH_PORT = 22
SSH_USERNAME = "reimis"  
SSH_PASSWORD = "ninjegos1" 
SSH_KEY_PATH = None 

# Sukuriame SSH klientą
def create_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if SSH_KEY_PATH:
            client.connect(SSH_HOST, SSH_PORT, SSH_USERNAME, key_filename=SSH_KEY_PATH)
        else:
            client.connect(SSH_HOST, SSH_PORT, SSH_USERNAME, password=SSH_PASSWORD)
        return client
    except paramiko.AuthenticationException:
        print(f"SSH autentifikacijos klaida: neteisingas vartotojo vardas arba slaptažodis")
        return None
    except Exception as e:
        print(f"SSH prisijungimo klaida: {e}")
        return None

def get_directory_contents():
    """Nuskaito esamos direktorijos turinį Linux serveryje"""
    client = create_ssh_client()
    if not client:
        return {"error": "Nepavyko prisijungti prie SSH serverio"}
    try:
        stdin, stdout, stderr = client.exec_command("ls -l")
        contents = stdout.read().decode().strip().split("\n")
        stdin, stdout, stderr = client.exec_command("pwd")
        directory = stdout.read().decode().strip()
        client.close()
        return {"directory": directory, "contents": contents}
    except Exception as e:
        client.close()
        return {"error": str(e)}

def get_ip_addresses():
    """Nuskaito sistemos IP adresus Linux serveryje"""
    client = create_ssh_client()
    if not client:
        return {"error": "Nepavyko prisijungti prie SSH serverio"}
    try:
        stdin, stdout, stderr = client.exec_command("ip addr show")
        ip_addresses = stdout.read().decode().strip()
        client.close()
        return {"ip_addresses": ip_addresses}
    except Exception as e:
        client.close()
        return {"error": str(e)}

def get_free_memory():
    """Nuskaito laisvą sistemos atmintį Linux serveryje"""
    client = create_ssh_client()
    if not client:
        return {"error": "Nepavyko prisijungti prie SSH serverio"}
    try:
        stdin, stdout, stderr = client.exec_command("free -b")
        memory_output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        client.close()
        if error:
            return {"error": f"Komandos vykdymo klaida: {error}"}
        lines = memory_output.split("\n")
        if len(lines) < 2:
            return {"error": "Netikėtas 'free' komandos formatas: per mažai eilučių"}
        for line in lines:
            if line.startswith("Mem:"):
                # Naudojame re.split, kad padalintume pagal kelis tarpus
                values = re.split(r'\s+', line.strip())
                if len(values) < 6:
                    return {"error": f"Netikėtas 'free' komandos formatas, per mažai stulpelių: {line}"}
                try:
                    return {
                        "total": int(values[1]),
                        "used": int(values[2]),
                        "free": int(values[3]),
                        "shared": int(values[4]),
                        "buff_cache": int(values[5]),
                        "available": int(values[6]) if len(values) > 6 else int(values[3]),
                        "percent": round((int(values[2]) / int(values[1])) * 100, 1)
                    }
                except (ValueError, IndexError) as e:
                    return {"error": f"Klaida apdorojant atminties informaciją: {str(e)}"}
        return {"error": f"Nerasta 'Mem:' eilutė: {memory_output}"}
    except Exception as e:
        client.close()
        return {"error": str(e)}

def create_file():
    """Sukuria naują failą su atsitiktiniu turiniu Linux serveryje"""
    client = create_ssh_client()
    if not client:
        return {"error": "Nepavyko prisijungti prie SSH serverio"}
    try:
        filename = "test_file.txt"
        content_length = random.randint(10, 50)
        random_content = ''.join(random.choices(string.ascii_letters + string.digits, k=content_length))
        command = f"echo '{random_content}' > {filename}"
        stdin, stdout, stderr = client.exec_command(command)
        error = stderr.read().decode().strip()
        client.close()
        if error:
            return {"error": f"Failo kūrimo klaida: {error}"}
        return {"message": f"Failas {filename} sukurtas sėkmingai", "content": random_content}
    except Exception as e:
        client.close()
        return {"error": str(e)}

def get_free_disk_space():
    """Nuskaito laisvą disko vietą Linux serveryje"""
    client = create_ssh_client()
    if not client:
        return {"error": "Nepavyko prisijungti prie SSH serverio"}
    try:
        stdin, stdout, stderr = client.exec_command("df -h")
        disk_output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        client.close()
        if error:
            return {"error": f"Komandos vykdymo klaida: {error}"}
        lines = disk_output.split("\n")
        if len(lines) < 2:
            return {"error": "Netikėtas 'df' komandos formatas: per mažai eilučių"}
        disks = []
        for line in lines[1:]:
            values = line.split()
            if len(values) >= 6:
                disks.append({
                    "filesystem": values[0],
                    "size": values[1],
                    "used": values[2],
                    "available": values[3],
                    "use_percent": values[4],
                    "mounted_on": " ".join(values[5:])
                })
            else:
                print(f"Praleista netinkama eilutė: {line}")
        return {"disks": disks} if disks else {"error": "Nerasta disko informacijos"}
    except Exception as e:
        client.close()
        return {"error": str(e)}
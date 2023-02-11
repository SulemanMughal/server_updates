import winrm
import uuid


def generate_flag(floating_ip=None, username=None, password=None):
    print("--> Generate Random Flags")
    flag = "{" + str(uuid.uuid4()).replace("-", "") + "}"
    try:
        s = winrm.Session(floating_ip, auth=(username, password))
        filename = fr'C:\Users\{username}\Desktop\root.txt'
        r = s.run_cmd(
            fr'echo flag{flag} > {filename}')
    except Exception as e:
        print("--> Exception", e)
    return flag

import smbclient.shutil
import uuid
import requests
from django.conf import settings


def openstack_authentication():
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'auth': {
            'identity': {
                'methods': [
                    'password',
                ],
                'password': {
                    'user': {
                        'name': settings.OPENSTACK_USER,
                        'domain': {
                            'id': 'default',
                        },
                        'password': settings.OPENSTACK_PASSWORD,
                    },
                },
            },
            "scope": {
                "project": {
                    "name": "admin",
                    "domain": {"id": "default"}
                }
            }

        },
    }
    s = requests.Session()
    response = s.post(settings.OPENSTACK_AUTHORIZED_URL,
                      headers=headers, json=json_data)
    if response.status_code in [200, 201, 202]:
        return response.headers["x-subject-token"]
    return None


def get_instance_users(imageRef=None):
    users_list = []
    try:
        token = openstack_authentication()
        if token:
            headers = {
                'X-Auth-Token': f'{token}',
            }
            s = requests.Session()
            response = s.get(
                f'{settings.OPENSTACK_IMAGE_URL}/{imageRef}', headers=headers)
            if response.status_code in [200, 201, 202]:
                for i in response.json():
                    if i[:5].lower() == "vuser":
                        users_list.append(
                            tuple(str(response.json()[i]).split(",")))
                return users_list
            return None
        else:
            print("--> OpenStack Authentication Failed")
            return None
    except Exception as e:
        print("--> Exception Occured")
        print(e)
        return None


def generate_flag(host=None, username=None, password=None):
    flag_value = str(uuid.uuid4()).replace("-", "")
    filename = "flag.txt"
    with open(filename, 'w') as f:
        f.write(str(flag_value))
    src = "" / settings.BASE_DIR / filename / ""
    dst = "\\\\" + host + "\\Desktop\\flag.txt"
    # print(src, dst, username, password)
    try:
        smbclient.shutil.copyfile(
            src,
            dst,
            username=username,
            password=password
        )
    except Exception as e:
        print(e)
        return None

    return flag_value


def copy_file(host=None, imageRef=None):
    users_list = get_instance_users(imageRef=imageRef)
    flag_list = []
    print(users_list)
    try:
        if users_list:
            for i in users_list:
                print(i)
                flag = generate_flag(
                    host, username=i[0].strip(), password=i[1].strip())
                # print(flag)
                if not flag:
                    print("--> Flags Not Updated For User : ", i)
                    return None
                flag_list.append(flag)
        return flag_list
    except Exception as e:
        print(e)

        return None
    return None

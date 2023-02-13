from django.conf import settings
import requests


def build_server(imageRef=None, server_id=None):
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
    headers = {
        'X-Auth-Token': f'{response.headers["x-subject-token"]}',
    }
    json_data = {
        "rebuild": {
            "imageRef":  imageRef
        }
    }

    response = s.post(f'{settings.OPENSTACK_SERVER_URL}/{server_id}/action',
                      headers=headers, json=json_data)

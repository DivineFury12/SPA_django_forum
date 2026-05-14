#!/usr/bin/env python

import subprocess
import json


def get_pid_app(name_app: str) -> str:
    raw_id_app = subprocess.run(
        f'tasklist | findstr {name_app}.exe',
        shell=True,
        capture_output=True,
        text=True,
    )
    id_app = raw_id_app.stdout.strip().split()[1]
    return id_app


def get_ips_app(pid: str) -> list[str]:
    result = subprocess.run(
        f'netstat -ano | findstr "{pid}"',
        shell=True,
        capture_output=True,
        text=True
    )
    raw_ips = [
        ip_el
        for i, ip_el in enumerate(result.stdout.split())
        if i % 5 == 2
    ]
    ips = list(set(ip_el.split(':')[0] for ip_el in raw_ips))
    return ips


def save_ips(ips: list[str]) -> None:
    data = []
    for ip in ips:
        data.append({
            'hostname': ip,
            'ip': '',
        })

    with open('amnezia_sites.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file)


if __name__ == '__main__':
    name_app = input()
    if not name_app:
        name_app = 'Telegram'

    pid = get_pid_app(name_app)
    ips = get_ips_app(pid)
    save_ips(ips)

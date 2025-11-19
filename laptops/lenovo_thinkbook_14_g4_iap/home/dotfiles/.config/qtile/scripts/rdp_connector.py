#!/usr/bin/env python3
import json
import subprocess
import os
from pathlib import Path

HOME_DIR = Path.home()
CONFIG_FILE = Path(HOME_DIR, '.config','rdp_connector.json')

def rofi_prompt(prompt, password=False):
    cmd = ['rofi', '-dmenu', '-p', prompt, '-lines', '0']
    if password:
        cmd.append('-password')
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError:
        return None

def get_connections():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def select_connection(connections) -> dict | None:
    names = [c['connection_name'] for c in connections]

    try:
        result = subprocess.check_output(
            ['rofi', '-dmenu', '-p', 'Select connection:'],
            input='\n'.join(names),
            text=True
        ).strip()
        connection = next(c for c in connections if c['connection_name'] == result)
    except subprocess.CalledProcessError:
        return None
    except StopIteration:
        return None

    return connection

def main():
    connections = get_connections()
    selected = select_connection(connections)
    if selected is None:
        return
    
    ip_address = selected.get('ip_address') or rofi_prompt(f'🌐 IP address for {selected["connection_name"]}')
    username = selected.get('username') or rofi_prompt(f'👤 Username for {selected["connection_name"]}')
    password = selected.get('password') or rofi_prompt(f'🔒 Password for {username}', password=True)

    
    params = selected.get('params') or rofi_prompt(f'⚙️ Additional params for {selected["connection_name"]}')
    
    if not all([username, password, ip_address]):
        return

    subprocess.run([
        'dunstify', '-t', '3000',
        'RDP Connection',
        f'🔄 Connecting to {ip_address} as {username}...'
    ])

    cmd = [
        'xfreerdp3',
        f'/u:{username}',
        f'/p:{password}',
        f'/v:{ip_address}',
        *params.split()
    ] if params else [
        'xfreerdp3',
        f'/u:{username}',
        f'/p:{password}',
        f"/v:{ip_address}"
        '/from-stdin'
    ]

    try:
        subprocess.run(
            cmd,
#            input=password + '\n',
            text=True,
            check=True
        )
        subprocess.run([
            'dunstify', '-u', 'normal',
            'RDP Connection',
            f'✅ Connected to {selected["connection_name"]}'
        ])
    except subprocess.CalledProcessError:
        subprocess.run([
            'dunstify', '-u', 'critical',
            'RDP Connection',
            f'❌ Failed to connect to {selected["connection_name"]}'
        ])

if __name__ == '__main__':
    main()

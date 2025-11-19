#!/usr/bin/env python3
import json
import subprocess
import threading
import os
import time
import shlex
from pathlib import Path

HOME_DIR = Path.home()
CONFIG_FILE = Path(HOME_DIR, ".config","rdp_connector.json")
FREE_CONN_NAME = "Connect to..."
FREE_CONN = {
    "connection_name": FREE_CONN_NAME,
    "username": None,
    "password": None,
    "ip_address": None,
    "params": "-grab-keyboard /dynamic-resolution"
}


class NonificationManager:
    """Notification class"""

    title = "RDP Connector"

    templates = {
        "closed": ("normal", "🔌 Connection {} was closed normally"),
        "connecting": ("normal", "🔄 Connecting to {}..."),
        "successful": ("normal", "✅ Connected to {}"),
        "failed": ("critical", "❌ Failed to connect to {}"),
        "lost": ("critical", "🚫 Connection {} lost"),
        "error": ("critical", "❌ Connection process was not started {}"),
        "started": ("normal", "✅ Monitoring process started {}")
    }

    @classmethod
    def _escape_for_dunst(cls, text:str ) -> str:
        """Replace "\" to "\\" """

        return text.replace("\\", "\\\\")

    @classmethod
    def send(cls, notification_type, connection_name):
        """Sending a notification"""

        severity, template = cls.templates[notification_type]
        message = template.format(cls._escape_for_dunst(connection_name))

        cmd = f"dunstify -u {severity} '{cls.title}' '{message}'"
        subprocess.run(shlex.split(cmd))


def rofi_prompt(prompt, password=False):
    """Prompting a parameter"""

    cmd = ["rofi", "-dmenu", "-p", prompt, "-lines", "0"]
    if password:
        cmd.append("-password")
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError:
        return None

def get_connections():
    """Reading config files"""
    with open(CONFIG_FILE) as f:
        return json.load(f)

def select_connection(connections) -> dict | None:
    """Selecting a connection from the list"""

    names = sorted([c["connection_name"] for c in connections])
    names.append(FREE_CONN_NAME)

    try:
        result = subprocess.check_output(
            ["rofi", "-i", "-dmenu", "-p", "Select connection:"],
            input="\n".join(names),
            text=True
        ).strip()
        if result == FREE_CONN_NAME:
            return FREE_CONN
        connection = next(c for c in connections if c["connection_name"] == result)
    except subprocess.CalledProcessError:
        return None
    except StopIteration:
        return None

    return connection

def check_connection_status(
        process: subprocess.Popen, 
        connection_name: str, ip_address: str, time_out: int = 2
):
    """Checking connection status"""

    time.sleep(time_out)
    
    if process.poll() is None:
        NonificationManager.send("successful", f"{connection_name} {ip_address}")
    
    exit_code = process.wait()

    if exit_code == 0 or exit_code == 12:
        NonificationManager.send("closed", f"{connection_name} - {ip_address}")
    elif exit_code == 141:
        NonificationManager.send("failed", f"{connection_name} - {ip_address}")
    elif exit_code == 147:
        NonificationManager.send("lost", f"{connection_name} - {ip_address}")
    else:
        NonificationManager.send("failed", f"{connection_name} - {ip_address}")
    
def main():
    connections = get_connections()
    selected = select_connection(connections)
    if selected is None:
        return
    
    ip_address = (
        selected.get("ip_address") or
        rofi_prompt(f"🌐 IP address for {selected['connection_name']}")
    )
    username = (
        selected.get("username") or
        rofi_prompt(f"👤 Username for {selected['connection_name']}")
    )
    password = (
        selected.get("password") or
        rofi_prompt(f"🔒 Password for {username}", password=True)
    )
    params = (
        selected.get("params") or
        rofi_prompt(f"⚙️ Additional params for {selected['connection_name']}")
    )
    
    if not all([username, password, ip_address]):
        return

    NonificationManager.send(
        "connecting",f"{selected['connection_name']} - {ip_address} as {username}"
    )

    cmd = [
        "xfreerdp3",
        f"/u:{username}",
        f"/p:{password}",
        f"/v:{ip_address}",
        *params.split()
    ] if params else [
        "xfreerdp3",
        f"/u:{username}",
        f"/p:{password}",
        f"/v:{ip_address}"
        "/from-stdin"
    ]

    try:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
        check_connection_status(process, selected["connection_name"], selected["ip_address"])
    except subprocess.CalledProcessError:
        NonificationManager.send("error", "")

if __name__ == "__main__":
    main()

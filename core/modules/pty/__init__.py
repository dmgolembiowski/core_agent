import os
import logging
import platform
import subprocess
from urllib import request

BUILDS_DIR = os.path.dirname(os.path.realpath(__file__))

class PTYController:
    def __init__(self, configs):
        self.start_agent()
        self.logger = configs["logger"]

    def stop_running_agent(self):
        try:
            running_pid = subprocess.check_output(["sudo", "fuser", "8998/tcp"], stderr=subprocess.DEVNULL).decode()
        except:
            print("couldn't get running pid")
            return

        os.system(f"sudo kill -9 {running_pid}")
        print("killed process")

        return


    def start_agent(self):
        processor_architecture = platform.machine()

        if not os.path.exists(f"{BUILDS_DIR}/{processor_architecture}"):
            print("platform not supported")
            return

        self.stop_running_agent()
        print("started go agent ", f"{BUILDS_DIR}/{processor_architecture}")
        os.system(f"{BUILDS_DIR}/{processor_architecture} &")


    def request(self, data):
        if type(data) != bytes:
            data = data.encode()

        response = request.urlopen("http://localhost:8998", data)
        response = response.read()

        return response
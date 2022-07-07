import os
from subprocess import check_output, call

if not os.path.exists("/opt/sixfab/core/.fixes"):
    os.system("sudo touch /opt/sixfab/core/.fixes")


def execute_fix(name, command):
    if name in fixes_list:
        return

    os.system("echo {} | sudo tee -a /opt/sixfab/core/.fixes".format(name))
    call(command, shell=True, executable='/bin/bash')

try:
    fixes_list = check_output(["sudo", "cat", "/opt/sixfab/core/.fixes"]).decode().split("\n")
except:
    fixes_list = []


# change old service file with new one
execute_fix("190320-manager-ifmetric", r'while :;do command -v ifmetric;if [ $? -eq "0" ];then sudo systemctl restart core_manager;break;fi;sudo apt-get install ifmetric -y;done')
execute_fix("150421-plugdev-group.2", r'PERMISSIONS_TO_ADD="SUBSYSTEM==\"usb\", ENV{DEVTYPE}==\"usb_device\", MODE=\"0664\", GROUP=\"plugdev\"";PLUGDEV_RULES_PATH=/etc/udev/rules.d/plugdev_usb.rules;if [ ! -f $PLUGDEV_RULES_PATH ];then echo $PERMISSIONS_TO_ADD|sudo tee $PLUGDEV_RULES_PATH>/dev/null 2>&1;sudo udevadm control --reload;sudo udevadm trigger;fi;sudo usermod -aG gpio sixfab>/dev/null 2>&1;sudo usermod -aG plugdev sixfab>/dev/null 2>&1;sudo systemctl restart core_manager')
execute_fix("301021-install-route", r'while :;do command -v route;if [ $? -eq "0" ];then sudo systemctl restart core_manager;break;fi;sudo apt-get install net-tools -y;done')
execute_fix("301021-install-lshw", r'while :;do command -v lshw;if [ $? -eq "0" ];then sudo systemctl restart core_manager;break;fi;sudo apt-get install lshw -y;done')
execute_fix("081021-update-atcomv2", r'sudo pip3 install -U --git+https://github.com/dmgolembiowski/atcom.git')
execute_fix("281221-env-file-permission", r'sudo chown -R sixfab:sixfab /opt/sixfab/.env.yaml')

import yaml
import pathlib
import getpass
import sys
def build_config():
    print("===== Building Config =====")
    p = pathlib.Path('config/server.yaml')
    with p.open(mode='r') as f:
        config = yaml.safe_load(f)
    for key in config:
        print(f"Setting Up {key}")
        for key2 in config[key]:
            custom_setting= input(f"What do you want to set for {key2}. Press enter to set the default of: {config[key][key2]}\n")
            if custom_setting:
                config[key]=custom_setting
    with p.open(mode="w") as f:
        documents = yaml.dump(config, f)

def build_service():
    print("===== Building Service file =====")
    p = pathlib.Path('temppi_web.service')
    cwd = pathlib.Path.cwd()
    user= getpass.getuser()
    with p.open(mode="w") as f:
        f.write(f"[Unit] \nDescription=TempPi Webserver\nAfter=network.target\n\n[Service]\nType=simple\nUser={user}\nWorkingDirectory=%s\nExecStart={sys.executable} {cwd}/server.py \nRestart=on-failure \n[Install]\nWantedBy=multi-user.target")
    print("Created a service file in current directory. Please copy this to /etc/systemd/system/")

print("Setting Up TempPi's Webserver")
build_config()
build_service()
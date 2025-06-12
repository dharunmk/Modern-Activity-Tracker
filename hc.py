from datetime import datetime
import os,subprocess
from time import sleep
from dotenv import load_dotenv
# load_dotenv()

def toggle_fan():
    # return
    with open('.env') as file:
        cmd = file.read().strip()
    with open('ip.txt') as file:
        ip = file.read().strip()
    cmd = cmd.replace('{ip}',ip)
    # subprocess.call(cmd,shell=True)
    # capture output
    for i in range(5):
        output = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE).stdout.decode('utf-8')
        if 'Unable to discover the device' not in output:
            break
        import ipr
        ipr.resolve_ip()
        sleep(1)

    with open('logs.txt','a') as file:
        print(datetime.now().strftime('%d-%b-%Y %I:%M:%p'),output,file=file)
    return 'Fan toggled'

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(toggle_fan())
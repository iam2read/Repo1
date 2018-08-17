# Requirements: Python 3
# Extra Modules:
#   pip install paramiko xlwt

import paramiko
import re
import xlwt
import os

# team_list = ['punvmlincor18.dsone.3ds.com','punvmlincor19.dsone.3ds.com']
team_list = ['punvmlincor18.dsone.3ds.com',
'punvmlincor19.dsone.3ds.com',
'punvmlincor20.dsone.3ds.com',
'punvmlincor21.dsone.3ds.com',
'punvmlincor26.dsone.3ds.com',
'punvmlincor27.dsone.3ds.com',
'punvmlincor28.dsone.3ds.com',
'punvmlincor29.dsone.3ds.com',
'punvmlincor22.dsone.3ds.com',
'punvmlincor23.dsone.3ds.com',
'punvmlincor24.dsone.3ds.com',
'punvmlincor25.dsone.3ds.com',
'punvmlincor30.dsone.3ds.com',
'punvmlincor31.dsone.3ds.com',
'punvmlincor32.dsone.3ds.com',
'punvmlincor32.dsone.3ds.com',
'punvmlincor45.dsone.3ds.com',
'punvmlincor34.dsone.3ds.com',
'punvmlincor35.dsone.3ds.com',
'punvmlincor36.dsone.3ds.com',
'punvmlincor37.dsone.3ds.com',
'punvmlincor38.dsone.3ds.com',
'punvmlincor39.dsone.3ds.com',
'punvmlincor40.dsone.3ds.com',
'punvmlincor41.dsone.3ds.com',
'punvmlincor42.dsone.3ds.com',
'punvmlincor43.dsone.3ds.com',
'punvmlincor44.dsone.3ds.com',
'punvmlincor15.dsone.3ds.com',
'punvmlincor15.dsone.3ds.com',
'punvmlincor16.dsone.3ds.com',
'punvmlincor14.dsone.3ds.com',
'punvmlincor17.dsone.3ds.com']







team_result = {}



command_list = {}
command_list['NIS Configuration'] = {}
command_list['NIS Configuration']['command'] = 'ypcat hosts'
command_list['NIS Configuration']['regex'] = '\d+\.\d+\.\d+\.\d+'

command_list['Access to /home/lego/ITtools'] = {}
command_list['Access to /home/lego/ITtools']['command'] = 'if [ -d "/home/lego/ITtools/PEOTE80/" ]; then\n echo fine\n else\n echo dead\n fi'
command_list['Access to /home/lego/ITtools']['regex'] = 'fine'

command_list['Access to /home/lego/ITSBWS'] = {}
command_list['Access to /home/lego/ITSBWS']['command'] = 'if [ -d "/home/lego/ITSBWS/Linux/" ]; then\n echo fine\n else\n echo dead\n fi'
command_list['Access to /home/lego/ITSBWS']['regex'] = 'fine'

command_list['Access to /home/lego/ITSBPrereq'] = {}
command_list['Access to /home/lego/ITSBPrereq']['command'] = 'if [ -d "/home/lego/ITSBPrereq/RnD_preq_18xFD03/" ]; then\n echo fine\n else\n echo dead\n fi'
command_list['Access to /home/lego/ITSBPrereq']['regex'] = 'fine'

command_list['Access to /home/lego/store'] = {}
command_list['Access to /home/lego/store']['command'] = 'if [ -d "/home/lego/store/PEO/" ]; then\n echo fine\n else\n echo dead\n fi'
command_list['Access to /home/lego/store']['regex'] = 'fine'

command_list['RHEL Version'] = {}
command_list['RHEL Version']['command'] = 'cat /etc/redhat-release'
command_list['RHEL Version']['regex'] = '.*7\.1.*'

command_list['Static IP Address'] = {}
command_list['Static IP Address']['command'] = 'cat /etc/sysconfig/network-scripts/ifcfg-eno16780032'
command_list['Static IP Address']['regex'] = 'BOOTPROTO=\d+\.\d+\.\d+\.\d+'

command_list['Access to TCK Tools'] = {}
command_list['Access to TCK Tools']['command'] = 'cat /u/env/tools/tck_init'
command_list['Access to TCK Tools']['regex'] = '.*set -x.*'

for team_server in team_list:
    print(team_server)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(team_server,username = 'root',password = '3dplmadmin')
    except paramiko.AuthenticationException:
        print("Authentication failed when connecting to %s" % team_server)
        sys.exit(1)
    server_result = {}
    for to_check, parameters_actions in command_list.items():
        try :
            print(team_server + ' !! ' + to_check)
            server_result[to_check] = 'KO'
            stdin, stdout, stderr = ssh.exec_command(parameters_actions['command'])
            stdout_readable = ''.join(stdout.readlines())
            print(stdout_readable)
            pattern = re.compile(parameters_actions['regex'])
            if pattern.match(stdout_readable):
                server_result[to_check] = 'OK'
        except:
            print('error!')
    
    team_result[team_server] = server_result


print(team_result)
import xlwt
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1",cell_overwrite_ok=True)

iRow = 2
iColumn = 2
for server, audit_actions in team_result.items():
    sheet1.write(iRow, iColumn, server)
    for audit_action, audit_status in audit_actions.items():
        iColumn = iColumn + 1
        sheet1.write(iRow, iColumn, audit_status)
        sheet1.write(1, iColumn, audit_action)
    iRow = iRow + 1
    iColumn = 2
if os.path.isfile("team.xls"):
    os.remove("team.xls")
book.save("team.xls")
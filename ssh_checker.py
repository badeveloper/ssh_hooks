import paramiko
import re
from itertools import izip

DF_CMD='df -hP'
CAT_SCSI_FILE='cat /proc/scsi/scsi'

LS_SCSI_PATH = 'ls /sys/bus/scsi/devices/'

def cmd_runner(ssh_client=None, cmd_args=None):
    if ssh_client:
        stdin, stdout, stderr = ssh_client.exec_command(cmd_args)
        cmd_output = stdout.readlines()
        return cmd_output

def df_output_parser(df_output=None):
    if df_output:
        one_dev = {}
        df_info = {}
        for i in df_output[1:]:
            oneline = re.split(' *', i.strip('\n'))
            blk_dev_name = oneline[0]
            fs_size_gb = oneline[1]
            fs_used_gb = oneline[2]
            fs_avail_gb = oneline[2]
            fs_use_ps = oneline[3]
            fs_mount_point = oneline[4]

            one_dev.update({blk_dev_name: {'fs_size': fs_size_gb, 'fs_used_gb': fs_used_gb,
                                           'fs_avail_gb': fs_avail_gb, 'fs_use_ps': fs_use_ps,
                                           'fs_mount_point': fs_mount_point}})
            df_info.update({'devs': one_dev})
        return df_info

def get_scsi_path_linux(ls_scsi_path):
    all_path = {}
    path_count = 0
    for i in ls_scsi_path:
        one_sub_folder =  i.strip('\n')
        scsi_path = re.search('^\d:\d:\d:\d', one_sub_folder)
        if scsi_path:
            scsi_path =  scsi_path.group()
            path_count += 1
            all_path.update({path_count: scsi_path})
    return all_path


def get_scsi_summ_linux(cat_scsi_file):
    scsci_summary = {}
    advanced_info = {}
    all = []
    iter1 = iter(cat_scsi_file[1:])
    for a, b, c in izip(iter1, iter1, iter1):
        all.append([a, b, c])
    # for i in cat_scsi_file[1:]:
    #     #print i
    #     split_line =  re.split(' *', i)
    #
    #     scsi_host =None
    #     if split_line[0] == 'Host:':
    #         scsi_host = split_line[1]
    #     scsi_channel = None
    #     if split_line[2] == 'Channel:':
    #         scsi_channel = split_line[3]
    #     scsi_id = None
    #     if split_line[4] == 'Id:':
    #         scsi_id = split_line[5]
    #     lun = None
    #     if split_line[6] == 'Lun:':
    #        lun = split_line[7]
    #     vendor_name =None
    #     if split_line[1] == 'Vendor:':
    #      vendor_name = split_line[2]
    #     model_name =None
    #     if split_line[3] == 'Model:':
    #        model_name = split_line[4]
    #     type =None
    #     if split_line[1] == 'Type:':
    #         type = split_line[2]

        # if scsi_host and scsi_channel and scsi_id and lun:
        #     scsi_host_number = re.search('\d$', scsi_host)
        #     if scsi_host_number:
        #         strict_path = scsi_host_number.group() + ':' + scsi_channel + ':' + scsi_id + ':' + lun
        #         full_path = {'scsi_host': scsi_host, 'scsi_channel': scsi_channel, 'scsi_id': scsi_id, 'scsi_lun': lun}
        #     if vendor_name and model_name:
        #             advanced_info.update({'vendor_name': vendor_name, 'model_name': model_name})
        #
        # scsci_summary.update({strict_path: full_path, 'adv': advanced_info})

    return all


def get_host_info(ssh_host=None, ssh_user=None, ssh_port=22, ssh_password=None, ssh_key=None, host_os=None):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if ssh_key:
        key = paramiko.RSAKey.from_private_key(open(ssh_key, 'ra'))
        ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=key, password=ssh_password)
    else:
        ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

    scsi_output = cmd_runner(ssh_client=ssh_client, cmd_args=CAT_SCSI_FILE)
    s = get_scsi_summ_linux(scsi_output)

    return s

scsi_info =  get_host_info(ssh_host='localhost', ssh_user='USER', ssh_password='PASSWORD')

for i in  scsi_info:
    print i








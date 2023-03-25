# -*- coding: utf-8 -*-

import json
import sys

def main():
    args = sys.argv

    if len(args) != 2 :
        print('inform ndt result file location')
        return

    msm_list = []
    with open(args[1], 'r') as f:
        for jo in f:
            msm_dict = json.loads(jo)
            msm_list.append(msm_dict)
    f.close()

    for line in msm_list:
        if 'Key' not in line:
            continue
        if line['Key'] == 'connected' and line['Value']['Test'] == 'download':
            print(line['Value']['Server'])
            break

if __name__ == "__main__":
    main()


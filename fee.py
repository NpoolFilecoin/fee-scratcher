import sys
import requests
import os
from tabulate import tabulate


def main() -> int:
    miner = 'f0111584'
    pageSize = 100
    startHeight = 1176254
    totalConsume = 0
    lastHeight = -1

    r = requests.post(
            'https://api.filscout.com/api/v1/transaction/count',
            json={'address': miner})
    for page in range(r.json()['data'] // pageSize + 1):
        r = requests.post(
                'https://api.filscout.com/api/v1/transaction',
                json={
                    'address': miner,
                    'idAddress': '',
                    'pageIndex': page,
                    'pageSize': pageSize})
        for data in r.json()['data']:
            if data['height'] < startHeight:
                break

            if lastHeight <= data['height'] and 0 <= lastHeight:
                continue

            print('cid: ', data['cid'], '   height', data['height'])

            if data['cid'] == 'N/A':
                print(' ', data['type'], data['value'])
                continue

            r1 = requests.get(os.path.join('https://api.filscout.com/api/v1/transaction', data['cid']))
            # r2 = requests.get(os.path.join('https://api.filscout.com/api/v1/message', data['cid']))
            dataArray = []
            for data1 in r1.json()['data']:
                value = 0
                if 'nano' in data1['value']:
                    value = float(data1['value'].replace('nanoFIL', '').replace(',', '').strip()) / 1000000000
                else:
                    value = data1['value'].replace('FIL', '').replace(',', '').strip()

                dataArray.append([data1['from'], data1['to'], data1['value'], data1['isPenalty'], data1['type']])
                totalConsume += float(value)

            print(tabulate(dataArray, headers=['from', 'to', 'value', 'penalty', 'type'], tablefmt='orgtbl'))

            lastHeight = data['height']

    print('{} consume {} FIL from {}' . format(miner, totalConsume, startHeight))


if __name__ == '__main__':
    sys.exit(main())

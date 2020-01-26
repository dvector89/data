import requests
import csv
import os
import sys

def get_data():
    url = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579579384&enterid=1579579384&from=timeline&isappinstalled=0'
    r = requests.get(url)
    txt = r.content.decode('utf-8')
    mark0 = 'window.getAreaStat = '
    mark1 = '}catch(e){}'

    begin = txt.find(mark0)
    end = txt.find(mark1, begin)

    data = txt[begin+len(mark0): end]

    return eval(data)

def save_csv(data, out_dir):
    for province in data:
        file_name = os.path.join(out_dir, province['provinceName']+'.csv')
        with open(file_name, 'w') as fid:
            fieldnames = ['city', 'number']
            writer = csv.DictWriter(fid, fieldnames=fieldnames)
            writer.writeheader()

            if len(province['cities']) < 1:
                writer.writerow({fieldnames[0]: province['provinceName'], 
                                 fieldnames[1]: province['confirmedCount']})
            for city in province['cities']:
                writer.writerow({fieldnames[0]: city['cityName'], 
                                 fieldnames[1]: city['confirmedCount']})
    return


def test(out_dir):
    data = get_data()
    save_csv(data, out_dir)



if __name__ == '__main__':
    out_dir = sys.argv[1]
    test(out_dir)

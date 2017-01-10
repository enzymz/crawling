#!/usr/bin/env python3

import requests
import csv
from bs4 import BeautifulSoup as bs


def get_all_hos():
    r = requests.get(
    'http://www.healthfamily.co/danh-sach-benh-vien?p=1&r=1071').text
    soup = bs(r,'html.parser')
    lst_hos = []
    for link in soup.find_all('a',string=True):
        href = link.get('href')
        if href.find('/thong-tin') == 0:
            lst_hos.append(href)
    return lst_hos


def get_info_hos(start,end):
    hospitals = get_all_hos()
    i = 0
    ls_hos_detail = [
        ['NAME','ADDRESS','PHONE','DESCRIPTION','MLat','MLong','LINK'],
    ]
    for i in range(start,end):
        link = 'http://www.healthfamily.co' + hospitals[i]
        r = requests.get(link).text
        bsoup = bs(r, 'html.parser')
        try:
            add = r.split('fa-home')[1].split('Địa chỉ:')[1].split('</p>')[0]
            phone = r.split('fa-phone-sign')[1].split('Số điện thoại:')[1].split('</p')[0]
            pre_desc = r.split('fa-info-sign')[1].split('HealthFamily.co')[0]
            bs_desc = bs(pre_desc, 'html.parser').getText()
            desc = bs_desc.split('Giới thiệu:')[1].strip()
            maps_lat = r.split('google.maps.LatLng(')[1].split(',')[0]
            maps_long = r.split('google.maps.LatLng(')[1].split(',')[1].split(')')[0]
        except: continue
        hospital_name = r.split('function initialize()')[1].split('title: \'')[1].split('<br>')[0]
        ls_hos_detail.append([hospital_name, add, phone, desc, maps_lat, maps_long,link])
        print(i)
        i += 1
    return ls_hos_detail


def export_():
    start = args_input_start()
    end = args_input_end()
    hos_detail = get_info_hos(start,end)
    with open('/tmp/crawl12.csv','w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for val in hos_detail:
            writer.writerows([val])

def args_input_start():
    start = int(input('Put start range: '))
    return start

def args_input_end():
    end = int(input('Put end range: '))
    return end

if __name__ == "__main__":
    
    export_()


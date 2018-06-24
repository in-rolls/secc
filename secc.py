import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

OUTPUT_FILE = 'secc.csv'

class SECCScraper:
    def __init__(self,
                 base_url='http://164.100.129.6/netnrega/secc_list.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

        self.form_data = {
            '__EVENTVALIDATION': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEENCRYPTED': ''
        }

    def GetStateList(self):
        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            # get form data
            self.form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEENCRYPTED': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()[0]
            }

            # get state list
            options = Selector(text=ret.text).xpath('//select[@id="ddl_state"]/option').extract()

            state_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                state = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                state_list.append(state)

            return state_list
        else:
            print('failed to get state list')

    def GetDistrictList(self, state_value):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddl_state',
            '__EVENTVALIDATION': self.form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.form_data['__VIEWSTATE'],
            '__VIEWSTATEENCRYPTED': self.form_data['__VIEWSTATEENCRYPTED'],
            'ddl_state': state_value
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.district_form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEENCRYPTED': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()[0]
            }

            # get district list
            options = Selector(text=ret.text).xpath('//select[@id="ddl_dist"]/option').extract()

            district_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                district = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                district_list.append(district)

            return district_list
        else:
            print('failed to get district list')

    def GetBlkList(self, state_value, district_value):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddl_dist',
            '__EVENTVALIDATION': self.district_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.district_form_data['__VIEWSTATE'],
            '__VIEWSTATEENCRYPTED': self.district_form_data['__VIEWSTATEENCRYPTED'],
            'ddl_dist': district_value,
            'ddl_state': state_value
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.blk_form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEENCRYPTED': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()[0]
            }

            # get blk list
            options = Selector(text=ret.text).xpath('//select[@id="ddl_blk"]/option').extract()

            blk_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                blk = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                blk_list.append(blk)

            return blk_list
        else:
            print('failed to get blk list')

    def GetPanList(self, state_value, district_value, blk_value):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddl_blk',
            '__EVENTVALIDATION': self.blk_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.blk_form_data['__VIEWSTATE'],
            '__VIEWSTATEENCRYPTED': self.blk_form_data['__VIEWSTATEENCRYPTED'],
            'ddl_blk': blk_value,
            'ddl_dist': district_value,
            'ddl_state': state_value
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.pan_form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEENCRYPTED': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()[0]
            }

            # get blk list
            options = Selector(text=ret.text).xpath('//select[@id="ddl_pan"]/option').extract()

            pan_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                pan = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                pan_list.append(pan)

            return pan_list
        else:
            print('failed to get pan list')

    def SelectPan(self, state_value, district_value, blk_value, pan_value):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddl_pan',
            '__EVENTVALIDATION': self.pan_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.pan_form_data['__VIEWSTATE'],
            '__VIEWSTATEENCRYPTED': self.pan_form_data['__VIEWSTATEENCRYPTED'],
            'ddl_blk': blk_value,
            'ddl_dist': district_value,
            'ddl_pan': pan_value,
            'ddl_state': state_value
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.sel_pan_form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEENCRYPTED': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()[0]
            }
            return True
        else:
            print('failed to select pan')
            return False

    def GetSECCList(self, state, district, blk, pan, lang, radio):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddl_pan',
            '__EVENTVALIDATION': self.pan_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.pan_form_data['__VIEWSTATE'],
            '__VIEWSTATEENCRYPTED': self.pan_form_data['__VIEWSTATEENCRYPTED'],
            'Button1': 'submit',
            'ddl_blk': blk['value'],
            'ddl_dist': district['value'],
            'ddl_pan': pan['value'],
            'ddl_state': state['value'],
            'ddrows': '45',
            'RadioButtonList1': lang,
            'Rbtnlist': radio['value']
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # No Record Found !
            if len(Selector(text=ret.text).xpath('//span[@id="lbl_msg"]').extract()):
                # write data into output csv file
                data = []
                data.append(state['name'])
                data.append(district['name'])
                data.append(blk['name'])
                data.append(pan['name'])
                data.append(lang)
                data.append(radio['name'])
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                self.WriteData(data)
            # else
            else:
                # get summary information
                summary_tables = Selector(text=ret.text).xpath('//table[@style="border-collapse:collapse"]').extract()[0]
                hh_summary_auto_exclusion = ''
                if len(Selector(text=summary_tables).xpath('//tr[3]/td[1]/text()').extract()) > 0:
                    hh_summary_auto_exclusion =  Selector(text=summary_tables).xpath('//tr[3]/td[1]/text()').extract()[0]
                hh_summary_auto_inclusion = ''
                if len(Selector(text=summary_tables).xpath('//tr[3]/td[2]/text()').extract()) > 0:
                    hh_summary_auto_inclusion = Selector(text=summary_tables).xpath('//tr[3]/td[2]/text()').extract()[0]
                hh_summary_auto_other = ''
                if len(Selector(text=summary_tables).xpath('//tr[3]/td[3]/text()').extract()) > 0:
                    hh_summary_auto_other = Selector(text=summary_tables).xpath('//tr[3]/td[3]/text()').extract()[0]
                hh_summary_deprivation = ''
                if len(Selector(text=summary_tables).xpath('//tr[3]/td[4]/text()').extract()) > 0:
                    hh_summary_deprivation = Selector(text=summary_tables).xpath('//tr[3]/td[4]/text()').extract()[0]

                # get table list
                tables = Selector(text=ret.text).xpath('//table[@style="border-collapse:collapse "]').extract()
                for idx in range(2, len(tables)):
                    table = tables[idx]

                    # get trs
                    trs = Selector(text=table).xpath('//tr').extract()
                    if len(trs) < 3: continue

                    start_tr = 2
                    if idx == 2: start_tr = 1
                    village = ''
                    for idx1 in range(start_tr, len(trs)):
                        tr = trs[idx1]

                        # get tds
                        tds = Selector(text=tr).xpath('//td').extract()

                        if len(tds) == 2:
                            if len(Selector(text=tds[1]).xpath('//b/nobr/text()').extract()) > 0:
                                village = Selector(text=tds[1]).xpath('//b/nobr/text()').extract()[0]
                            continue
                        elif 'Village:' in Selector(text=tds[1]).xpath('//nobr/text()').extract()[0]:
                            village = Selector(text=tds[1]).xpath('//nobr/text()').extract()[0]
                            village = str(village).replace('Village:', '')
                            continue
                        else:
                            secc_info = {
                                'head_of_hh': Selector(text=tds[1]).xpath('//nobr/text()').extract()[0],
                                'gender': Selector(text=tds[2]).xpath('//text()').extract()[0],
                                'age': Selector(text=tds[3]).xpath('//nobr/text()').extract()[0] if len(Selector(text=tds[3]).xpath('//nobr/text()').extract()) > 0 else '',
                                'social_cat': Selector(text=tds[4]).xpath('//nobr/text()').extract()[0],
                                'fathers_and_mothers_name': Selector(text=tds[5]).xpath('//nobr/text()').extract()[0],
                                'deprivation_count': Selector(text=tds[6]).xpath('//nobr/text()').extract()[0],
                                'auto_inclusion_deprivation_code': Selector(text=tds[7]).xpath('//text()').extract()[0],
                                'total_members': Selector(text=tds[8]).xpath('//text()').extract()[0]
                            }

                            # write data into output csv file
                            data = []
                            data.append(state['name'])
                            data.append(district['name'])
                            data.append(blk['name'])
                            data.append(pan['name'])
                            data.append(lang)
                            data.append(radio['name'])
                            data.append(secc_info['head_of_hh'])
                            data.append(secc_info['gender'])
                            data.append(secc_info['age'])
                            data.append(secc_info['social_cat'])
                            data.append(secc_info['fathers_and_mothers_name'])
                            data.append(secc_info['deprivation_count'])
                            data.append(secc_info['auto_inclusion_deprivation_code'])
                            data.append(secc_info['total_members'])
                            data.append(hh_summary_auto_inclusion)
                            data.append(hh_summary_auto_exclusion)
                            data.append(hh_summary_auto_other)
                            data.append(hh_summary_deprivation)
                            data.append(village)
                            self.WriteData(data)
            return True
        else:
            print('failed to get SECC list')
            return False

    def WriteHeader(self):
        # set headers
        header_info = [
            'state',
            'district',
            'tehsil',
            'panchayat',
            'language',
            'auto_inclusion_deprivation_or_exclusion_or_other ',
            'head_of_hh',
            'gender',
            'age',
            'social_cat',
            'fathers_and_mothers_name',
            'deprivation_count',
            'auto_inclusion_deprivation_code',
            'total_members',
            'hh_summary_auto_inclusion',
            'hh_summary_auto_exclusion',
            'hh_summary_auto_other',
            'hh_summary_deprivation',
            'village'
        ]

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w', encoding='utf-8'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a', encoding='utf-8'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def Start(self,
              start_state='',
              start_district='',
              start_blk='',
              start_pan=''):
        # set radio buttons
        radiobuttons = [
            {'value': '0', 'name': 'Auto Inclusion or Deprivation'},
            {'value': '1', 'name': 'Auto Exclusion'},
            {'value': '2', 'name': 'Others'}
        ]

        # write header into output csv file
        if start_state == '' and True: self.WriteHeader()

        # get state list
        print('getting state list...')
        state_list = self.GetStateList()
        print(state_list)

        state_flag = False
        if start_state == '': state_flag = True

        district_flag = False
        if start_district == '': district_flag = True

        blk_flag = False
        if start_blk == '': blk_flag = True

        pan_flag = False
        if start_pan == '': pan_flag = True

        for state in state_list:
            if start_state == state['name']: state_flag = True
            if state_flag == False: continue

            # get district list
            print('getting district list for %s...' % (state['name']))
            district_list = self.GetDistrictList(state['value'])
            print(district_list)

            for district in district_list:
                if start_district == district['name']: district_flag = True
                if district_flag == False: continue

                # get blk list
                print('getting blk list for %s:%s...' % (state['name'], district['name']))
                blk_list = self.GetBlkList(state['value'], district['value'])
                print(blk_list)

                for blk in blk_list:
                    if start_blk == blk['name']: blk_flag = True
                    if blk_flag == False: continue

                    # get pan list
                    print('getting pan list for %s:%s:%s...' % (state['name'], district['name'], blk['name']))
                    pan_list = self.GetPanList(state['value'], district['value'], blk['value'])
                    print(pan_list)

                    for pan in pan_list:
                        if start_pan == pan['name']: pan_flag = True
                        if pan_flag == False: continue

                        # select pan
                        print('selecting pan for %s:%s:%s:%s...' % (state['name'], district['name'], blk['name'], pan['name']))
                        sel_flag = self.SelectPan(state['value'], district['value'], blk['value'], pan['value'])
                        print(sel_flag)

                        for radio in radiobuttons:
                            # get SECC list
                            print('getting SECC list for %s:%s:%s:%s:%s...' % (state['name'], district['name'], blk['name'], pan['name'], radio['name']))
                            ret_val = self.GetSECCList(state, district, blk, pan, 'eng', radio)
                            print(ret_val)

            #                 break
            #             break
            #         break
            #     break
            # break

def main():
    # create scraper object
    scraper = SECCScraper()

    # start to scrape
    scraper.Start(
        start_state='BIHAR',
        start_district='Katihar',
        start_blk='Azamnagar',
        start_pan='GORAKHPUR(GP)'
    )

if __name__ == '__main__':
    main()

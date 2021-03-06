#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""
Script to pull campaigns

"""

from includes.ActiveCampaign import ActiveCampaign
from includes.Config import ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY
import json
import argparse
import codecs
import sys

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# ---------------------------------------------------------------------------------------------------------------------
# VARS

campaign_paginator_path= './data/campaign_paginator.json'
campaign_list_path = './data/campaign_list.json'
campaign_report_open_lists_path = './data/campaign_report_open_lists.json'
campaign_report_unopen_lists_path = './data/campaign_report_unopen_lists.json'
campaign_report_link_lists_path = './data/campaign_report_link_lists.json'
campaign_report_unsubscribe_lists_path = './data/campaign_report_unsubscribe_lists.json'
campaign_report_forward_lists_path = './data/campaign_report_forward_lists.json'
list_paginator_path = './data/list_paginator.json'
list_list_path = './data/list_list.json'
contact_paginator_path = './data/contact_paginator.json'
contact_list_path = './data/contact_list.json'
# no paginator for message
message_list_path = './data/message_list.json'


# ---------------------------------------------------------------------------------------------------------------------
# UTILITY

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------------------------------------------------
# WRITE


# CAMPAIGN PAGINATOR
# Paginator is the action that returns a list of campaigns
def write_campaign_paginator():
    print 'Querying campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator_file = open(campaign_paginator_path, 'wb')
    campaign_paginator_dict = {'total':100}
    offset = 0
    while campaign_paginator_dict['total'] - offset > 0:
        campaign_paginator_dict = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
        print str(campaign_paginator_dict['total']) + 'campaigns found'
        for row in campaign_paginator_dict['rows']:
            campaign_paginator_file.write(json.dumps(row) + '\n')
            print row['id'] + ',' + row['uniqueopens']
        offset += 100

# CAMPAIGNS
def write_campaigns():
    # Paginator is the action that returns a list of campaigns
    print 'Querying campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    # commented out for campaign pagination support   
    # campaign_paginator_file = open(campaign_paginator_path, 'wb')
    # campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    # json.dump(campaign_paginator, campaign_paginator_file)
    # campaign_paginator_file.close()
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    campaign_list_file = open(campaign_list_path, 'wb')
    #for campaign_row in campaign_paginator['rows']:
    for campaign_row in campaign_rows:
        print 'Querying \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] +' ...'
        campaign_list =  ac.api('campaign/list?ids='+campaign_row['id'])
        json.dump(campaign_list, campaign_list_file)
        campaign_list_file.write('\n')
    campaign_list_file.close()
    print 'Done!'
    
def write_campaign_report_open_lists():
    # Paginator is the action that returns a list of campaigns
    print 'Querying campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    campaign_report_open_list_file = open(campaign_report_open_lists_path, 'wb')
    for campaign_row in campaign_rows:
        page = 0
        campaign_report_open_list = []
        while True: # there is no do ... while () loop in python
            page = page + 1
            print 'Querying open list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] + '; page='+str(page)+' ...'
            campaign_report_open_dict = ac.api('campaign/report_open_list?campaignid=' + campaign_row['id'] + '&page=' + str(page))
            have_opens = campaign_report_open_dict.pop('result_code')
            campaign_report_open_dict.pop('result_message')
            campaign_report_open_dict.pop('result_output')
            if have_opens == 0:
                break
            campaign_report_open_list.extend(list(campaign_report_open_dict.values()))
        out_dict = {'campaign_id':campaign_row['id']}  # store which campaign this list belongs to
        out_dict['open_list'] = campaign_report_open_list
        json.dump(out_dict, campaign_report_open_list_file)
        campaign_report_open_list_file.write('\n')
    campaign_report_open_list_file.close()
    print 'Done!'

 
def write_campaign_report_unopen_lists():
    print 'Querying campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    campaign_report_unopen_list_file = open(campaign_report_unopen_lists_path, 'wb')
    for campaign_row in campaign_rows:
        page = 0
        campaign_report_unopen_list = []
        while True: # there is no do ... while () loop in python
            page = page + 1
            print 'Querying unopen list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] + '; messageid='+ str(campaign_row['messageid']) +'; page='+str(page)+' ...'
            campaign_report_unopen_dict = ac.api('campaign/report_unopen_list?campaignid=' + campaign_row['id'] + '&messageid=' + str(campaign_row['messageid']) + '&page=' + str(page))
            have_unopens = campaign_report_unopen_dict.pop('result_code')
            campaign_report_unopen_dict.pop('result_message')
            campaign_report_unopen_dict.pop('result_output')
            if have_unopens == 0:
                break
            campaign_report_unopen_list.extend(list(campaign_report_unopen_dict.values()))
        out_dict = {'campaign_id':campaign_row['id']}  # store which campaign this list belongs to
        out_dict['open_list'] = campaign_report_unopen_list
        json.dump(out_dict, campaign_report_unopen_list_file)
        campaign_report_unopen_list_file.write('\n')
    campaign_report_unopen_list_file.close()
    print 'Done!'

def write_campaign_report_link_lists():
    # Paginator is the action that returns a list of campaigns
    print 'Querying campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    # commented out for campaign pagination support  
    #campaign_paginator_file = open(campaign_paginator_path, 'wb')
    #campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    #json.dump(campaign_paginator, campaign_paginator_file)
    #campaign_paginator_file.close()
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    campaign_report_link_list_file = open(campaign_report_link_lists_path, 'wb')
    #for campaign_row in campaign_paginator['rows']:
    for campaign_row in campaign_rows:
        print 'Querying link list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] + '; messageid='+ str(campaign_row['messageid']) +' ...'
        campaign_report_link_list = ac.api('campaign/report_link_list?campaignid=' + campaign_row['id'] + '&messageid=' + str(campaign_row['messageid']))
        json.dump(campaign_report_link_list, campaign_report_link_list_file)
        campaign_report_link_list_file.write('\n')
    campaign_report_link_list_file.close()
    print 'Done!'

def write_campaign_report_unsubscribe_lists():
    # Paginator is the action that returns a list of campaigns
    print 'Querying campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    # commented out for campaign pagination support    
    #campaign_paginator_file = open(campaign_paginator_path, 'wb')
    #campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    #json.dump(campaign_paginator, campaign_paginator_file)
    #campaign_paginator_file.close()
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    campaign_report_unsubscribe_list_file = open(campaign_report_unsubscribe_lists_path, 'wb')
    #for campaign_row in campaign_paginator['rows']:
    for campaign_row in campaign_rows:
        print 'Querying unsubscribe list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] +' ...'
        campaign_report_unsubscribe_list = ac.api('campaign/report_unsubscription_list?campaignid=' + campaign_row['id'])
        json.dump(campaign_report_unsubscribe_list, campaign_report_unsubscribe_list_file)
        campaign_report_unsubscribe_list_file.write('\n')
    campaign_report_unsubscribe_list_file.close()
    print 'Done!'


def write_campaign_report_forward_lists():
    # Paginator is the action that returns a list of campaigns
    print 'Querying campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    # commented out for campaign pagination support     
    #campaign_paginator_file = open(campaign_paginator_path, 'wb')
    #campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    #json.dump(campaign_paginator, campaign_paginator_file)
    #campaign_paginator_file.close()
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    campaign_report_forward_list_file = open(campaign_report_forward_lists_path, 'wb')
    #for campaign_row in campaign_paginator['rows']:
    for campaign_row in campaign_rows:
        print 'Querying link list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id']  + '; messageid='+ str(campaign_row['messageid']) +' ...'
        campaign_report_forward_list = ac.api('campaign/report_forward_list?campaignid=' + campaign_row['id']+ '&messageid=' + str(campaign_row['messageid']))
        json.dump(campaign_report_forward_list, campaign_report_forward_list_file)
        campaign_report_forward_list_file.write('\n')
    campaign_report_forward_list_file.close()
    print 'Done!'


# LISTS
def write_list_paginator():
    print 'Querying list paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    list_paginator_file = open(list_paginator_path, 'wb')
    list_paginator_dict = {'total':100}
    offset = 0
    while list_paginator_dict['total'] - offset > 0:
        list_paginator_dict = ac.api('list/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
        print str(list_paginator_dict['total']) + ' lists found'
        for row in list_paginator_dict['rows']:
            list_paginator_file.write(json.dumps(row) + '\n')
        offset += 100
        
def write_lists():
    print 'Querying list paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    # assume hard limit of 100
    list_paginator = ac.api('list/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    list_rows = list_paginator['rows']
    if list_paginator['total'] > 100:
        offset = 0
        while list_paginator['total'] - offset > 0:
            list_paginator = ac.api('list/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            list_rows.extend(list_paginator['rows'])
            offset += 100
    list_list_file = open(list_list_path, 'wb')
    for list_row in list_rows:
        print 'Querying \'' + list_row['name'] + '\'; id=' + list_row['id'] +' ...'
        list_list =  ac.api('list/list?ids='+list_row['id'])
        json.dump(list_list, list_list_file)
        list_list_file.write('\n')
    list_list_file.close()
    print 'Done!'

# TODO CONTACTS
def write_contact_paginator():
     # Paginator is the action that returns a list of campaigns
    print 'Querying contact paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    contact_paginator_file = open(contact_paginator_path, 'wb')
    contact_paginator = {'total':100}
    offset = 0
    while contact_paginator['total'] - offset > 0:
        print 'querying offset ' + str(offset) + ' out of ' + str(contact_paginator['total'])
        contact_paginator = ac.api('contact/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
        contact_rows = contact_paginator['rows']
        for contact in contact_rows:
            json.dump(contact, contact_paginator_file)
            contact_paginator_file.write('\n')
        offset += 100

def write_contacts():
    # NOTE:
    # write contacts work differently from the other paginator based queries
    # Instead of collecting the paginator in memory before running the detail API calls
    # the paginator has to be run separately. The paginator results are then read here from a file.
    print 'Reading contact paginator json ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    contact_paginator_file = open(contact_paginator_path, 'rb')
    contact_list_file = open(contact_list_path, 'wb')
    id_list = []
    total = 0
    i = 0
    for line in contact_paginator_file: # read and parse line by line
        contact_row = json.loads(line)
        # query 20 by 20
        i += 1
        total += 1
        if i <= 20:
            id_list.append(contact_row['id'])
        if i == 20:
            print 'Querying ids=' + ','.join(id_list) +' ...'
            contact_list = ac.api('contact/list?ids='+','.join(id_list))
            result_code = contact_list.pop('result_code')
            contact_list.pop('result_message')
            contact_list.pop('result_output')
            if result_code == 1:
                for contact in list(contact_list.values()):
                    json.dump(contact, contact_list_file)
                    contact_list_file.write('\n')
            i = 0
            id_list = []
    if len(id_list) > 0:  # repetitive code... ugly
        contact_list = ac.api('contact/list?ids='+','.join(id_list))
        result_code = contact_list.pop('result_code')
        contact_list.pop('result_message')
        contact_list.pop('result_output')
        if result_code == 1:
            for contact in list(contact_list.values()):
                json.dump(contact, contact_list_file)
                contact_list_file.write('\n')
    contact_paginator_file.close()
    contact_list_file.close()
    print 'Done!'
    
# MESSAGES
def write_message_lists():
    # No paginator in API but can request for all messages, subject to paging
    print 'Querying message list ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    page = 0
    message_list_file = open(message_list_path, 'wb')
    while True:
        page = page + 1
        message_dict = ac.api('message/list?ids=all&page=' + str(page))
        have_opens = message_dict.pop('result_code')
        message_dict.pop('result_message')
        message_dict.pop('result_output')
        for key in range(len(message_dict)):
            print 'Querying \'' + message_dict[str(key)]['subject'] + '\'; id=' + message_dict[str(key)]['id'] +' ...'
            message = ac.api('message/view?id=' + str(message_dict[str(key)]['id']))
            json.dump(message, message_list_file)
            message_list_file.write('\n')
        if have_opens == 0:
            break
    message_list_file.close()
    print 'Done!'

# ---------------------------------------------------------------------------------------------------------------------
# PRINT


# CAMPAIGNS
def print_campaigns():
    # Paginator is the action that returns a list of campaigns
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    for campaign_row in campaign_rows:
        print 'Querying \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] +' ...'
        campaign_dict =  ac.api('campaign/list?ids='+campaign_row['id'])

    print 'Done!'

# CAMPAIGN REPORT OPEN LIST
def print_campaign_report_open_lists():
    # Paginator is the action that returns a list of campaigns
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    for campaign_row in campaign_rows:
        page = 0
        while True: # there is no do ... while () loop in python
            page = page + 1
            campaign_report_open_dict = ac.api('campaign/report_open_list?campaignid=' + campaign_row['id'] + '&page=' + str(page))
            have_opens = campaign_report_open_dict.pop('result_code')
            campaign_report_open_dict.pop('result_message')
            campaign_report_open_dict.pop('result_output')
            if have_opens == 0:
                break
            for user_open in list(campaign_report_open_dict.values()):
                print campaign_row['id']+','+user_open['times']+','+user_open['tstamp']+','+user_open['subscriberid']+','+user_open['email']

# CAMPAIGN REPORT UNOPEN LIST
def print_campaign_report_unopen_lists():
    # Paginator is the action that returns a list of campaigns
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    for campaign_row in campaign_rows:
        page = 0
        while True: # there is no do ... while () loop in python
            page = page + 1
            campaign_report_unopen_dict = ac.api('campaign/report_unopen_list?campaignid=' + campaign_row['id'] + '&messageid=' + str(campaign_row['messageid']) + '&page=' + str(page))
            have_unopens = campaign_report_unopen_dict.pop('result_code')
            campaign_report_unopen_dict.pop('result_message')
            campaign_report_unopen_dict.pop('result_output')
            if have_unopens == 0:
                break
            for user_open in list(campaign_report_unopen_dict.values()):
                print campaign_row['id']+','+user_open['times']+','+user_open['tstamp']+','+user_open['orgname']+','+user_open['phone']+','+user_open['subscriberid']+','+user_open['email']


# CAMPAIGN REPORT LINK LIST    
def print_campaign_report_link_lists():
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    for campaign_row in campaign_rows:
        campaign_report_link_dict = ac.api('campaign/report_link_list?campaignid=' + campaign_row['id'] + '&messageid=' + str(campaign_row['messageid']))
        if campaign_report_link_dict['result_code'] == 1:
            for k in campaign_report_link_dict.keys():
                if is_int(k):
                    link_dict = campaign_report_link_dict[k]
                    if link_dict.has_key('info'):
                        for user_dict in link_dict['info']:
                            row_str = ''
                            row_str += campaign_row['id'] + ','
                            row_str += str(campaign_row['messageid']) + ','
                            row_str += link_dict.get('a_unique','') + ','
                            row_str += link_dict.get('tracked','') + ','
                            row_str += link_dict.get('link','') + ','
                            row_str += link_dict.get('a_total','') + ','
                            row_str += link_dict.get('id','') + ','
                            row_str += link_dict.get('name','') + ','
                            row_str += user_dict.get('subscriberid','') + ','
                            row_str += user_dict.get('orgname','') + ','
                            row_str += user_dict.get('times','') + ','
                            row_str += user_dict.get('phone','') + ','
                            row_str += user_dict.get('tstamp','') + ','
                            row_str += user_dict.get('email','')
                            print row_str
                    else:
                        row_str = ''
                        row_str += campaign_row['id'] + ','
                        row_str += str(campaign_row['messageid']) + ','
                        row_str += link_dict.get('a_unique','') + ','
                        row_str += link_dict.get('tracked','') + ','
                        row_str += link_dict.get('link','') + ','
                        row_str += link_dict.get('a_total','') + ','
                        row_str += link_dict.get('id','') + ','
                        row_str += link_dict.get('name','') + ',,,,,,'
                        print row_str

# CAMPAIGN REPORT UNSUBSCRIBE LIST    
def print_campaign_report_unsubscribe_lists():
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    #campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100    
    #for campaign_row in campaign_paginator['rows']:
    for campaign_row in campaign_rows:
        campaign_report_unsubscribe_dict = ac.api('campaign/report_unsubscription_list?campaignid=' + campaign_row['id'])
        if campaign_report_unsubscribe_dict['result_code'] == 1:
            for k in campaign_report_unsubscribe_dict.keys():
                if is_int(k):
                    unsub_dict = campaign_report_unsubscribe_dict[k]
                    row_str = ''
                    row_str += campaign_row['id'] + ','
                    row_str += unsub_dict.get('orgname','') + ','
                    unsub_reason = unsub_dict.get('unsubreason','')
                    row_str += (unsub_reason if unsub_reason != None else '') + ','
                    row_str += unsub_dict.get('udate','') + ','
                    row_str += unsub_dict.get('subscriberid','') + ','
                    row_str += unsub_dict.get('phone','') + ','
                    row_str += unsub_dict.get('tstamp','') + ','
                    row_str += unsub_dict.get('email','')
                    print row_str

# CAMPAIGN REPORT FORWARD LIST
def print_campaign_report_forward_lists():
    # Paginator is the action that returns a list of campaigns
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    campaign_paginator = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaign_paginator['rows']
    if campaign_paginator['total'] > 100:
        outstanding_campaigns = campaign_paginator['total'] - 100
        offset = 100
        while outstanding_campaigns > 0:
            campaign_paginator = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaign_paginator['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
    for campaign_row in campaign_rows:
        campaign_report_forward_dict = ac.api('campaign/report_forward_list?campaignid=' + campaign_row['id']+ '&messageid=' + str(campaign_row['messageid']))
        if campaign_report_forward_dict['result_code'] == 1:
            for k in campaign_report_forward_dict.keys():
                if is_int(k):
                    fwd_dict = campaign_report_forward_dict[k]
                    row_str = ''
                    row_str += campaign_row['id'] + ','
                    row_str += fwd_dict.get('a_times','') + ','
                    row_str += fwd_dict.get('subscriberid','') + ','
                    row_str += fwd_dict.get('brief_message','') + ','
                    row_str += fwd_dict.get('name_from','') + ','
                    row_str += fwd_dict.get('tstamp','') + ','
                    row_str += fwd_dict.get('email_to','') + ','
                    row_str += fwd_dict.get('messageid','') + ','
                    row_str += fwd_dict.get('email_from','')
                    print row_str

# LIST PAGINATOR
def print_list_paginator():
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    list_paginator_dict = {'total':100}
    offset = 0
    while list_paginator_dict['total'] - offset > 0:
        list_paginator_dict = ac.api('list/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
        for row in list_paginator_dict['rows']:
            print row['id']
        offset += 100

# LISTS
def print_lists():
    # Paginator is the action that returns a list of campaigns
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    list_paginator = ac.api('list/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    list_rows = list_paginator['rows']
    if list_paginator['total'] > 100:
        outstanding_lists = list_paginator['total'] - 100
        offset = 100
        while outstanding_lists > 0:
            list_paginator = ac.api('list/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            list_rows.extend(list_paginator['rows'])
            outstanding_lists = outstanding_lists - 100
            offset = offset + 100
    for list_row in list_rows:
        list_dict =  ac.api('list/list?ids='+list_row['id'])
        if list_dict['result_code'] == 1:
            for k in list_dict.keys():
                if is_int(k):
                    ls_dict = list_dict[k]
                    row_str = ''
                    row_str += ls_dict.get('name','') + ','
                    row_str += str(ls_dict.get('subscriber_count','')) + ','
                    row_str += ls_dict.get('userid','') + ','
                    row_str += ls_dict.get('private','') + ','
                    row_str += ls_dict.get('cdate','') + ','
                    row_str += ls_dict.get('id','')
                    print row_str

# CONTACTS
def print_contacts():
    # Paginator is the action that returns a list of campaigns
    print 'Querying contact paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    # commented out for campaign pagination support
    # contact_paginator_file = open(contact_paginator_path, 'wb')
    # contact_paginator = ac.api('contact/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    # json.dump(contact_paginator, contact_paginator_file)
    # contact_paginator_file.close()
    # assume hard limit of 100
    contact_paginator = ac.api('contact/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    contact_rows = contact_paginator['rows']
    if contact_paginator['total'] > 100:
        outstanding_contacts = contact_paginator['total'] - 100
        offset = 100
        while outstanding_contacts > 0:
            contact_paginator = ac.api('contact/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            contact_rows.extend(contact_paginator['rows'])
            outstanding_contacts = outstanding_contacts - 100
            offset = offset + 100
    contact_list_file = open(contact_list_path, 'wb')
    #for contact_row in contact_paginator['rows']:
    for contact_row in contact_rows:
        print 'Querying \'' + contact_row['name'] + '\'; id=' + contact_row['id'] +' ...'
        contact_list =  ac.api('contact/list?ids='+contact_row['id'])
        json.dump(contact_list, contact_list_file)
        contact_list_file.write('\n')
    contact_list_file.close()
    print 'Done!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Active Campaign')
    parser.add_argument('--mode', type=str, help="Accepted values: 'write' or 'print'")
    parser.add_argument('--info', type=str, help="Accepted values: 'campaigns', 'lists', 'campaign_report_bounce_list'")
    args = parser.parse_args() # parser.parse_args('--mode write --info contacts'.split())
    function_name = args.mode + '_' + args.info
    if function_name in dir():
        locals()[function_name]()
    else:
        print 'Argument combination not supported!'


    

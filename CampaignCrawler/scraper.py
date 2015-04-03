# -*- coding: utf-8 -*-
"""
Script to pull campaigns

"""

from includes.ActiveCampaign import ActiveCampaign
from includes.Config import ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY
import json
import argparse

# ---------------------------------------------------------------------------------------------------------------------
# VARS

campaign_paginator_path= './data/campaign_paginator.json'
campaign_list_path = './data/campaign_list.json'
campaign_report_open_lists_path = './data/campaign_report_open_lists.json'
campaign_report_link_lists_path = './data/campaign_report_link_lists.json'
campaign_report_unsubscribe_lists_path = './data/campaign_report_unsubscribe_lists.json'
campaign_report_forward_lists_path = './data/campaign_report_forward_lists.json'
list_paginator_path = './data/list_paginator.json'
list_list_path = './data/list_list.json'


# ---------------------------------------------------------------------------------------------------------------------
# UTILITY

def dict2csv(dictorlist):
    if type(dictorlist) is dict:
        print ', '.join(dictorlist.keys())
    elif type(dictorlist) is list:
        print ', '.join(dictorlist[0].keys())


# ---------------------------------------------------------------------------------------------------------------------
# WRITE

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
    campaign_report_open_list_file = open(campaign_report_open_lists_path, 'wb')
    #for campaign_row in campaign_paginator['rows']:
    for campaign_row in campaign_rows:
        print 'Querying open list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] +' ...'
        #campaign_report_open_dict = ac.api('campaign/report_open_list?campaignid=' + campaign_row['id'] + '&page=1')
        page = 0
        campaign_report_open_list = []
        while True: # there is no do ... while () loop in python
            page = page + 1        
            campaign_report_open_dict = ac.api('campaign/report_open_list?campaignid=' + campaign_row['id'] + '&page=' + str(page))
            have_opens = campaign_report_open_dict.pop('result_code')
            campaign_report_open_dict.pop('result_message')
            campaign_report_open_dict.pop('result_output')
            campaign_report_open_list.extend(list(campaign_report_open_dict.values()))
            if have_opens == 0:
                break
        # done?: TODO paginate if there are more pages in open lists
        out_dict = {'campaign_id':campaign_row['id']}  # store which campaign this list belongs to
        out_dict['open_list'] = campaign_report_open_list
        json.dump(out_dict, campaign_report_open_list_file)
        campaign_report_open_list_file.write('\n')
    campaign_report_open_list_file.close()
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
        print 'Querying link list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] +' ...'
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
def write_lists():
    print 'Querying list paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    list_paginator_file = open(list_paginator_path, 'ab')
    list_paginator = ac.api('list/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    # TODO paginate if there are more pages
    json.dump(list_paginator, list_paginator_file)
    list_paginator_file.close()
    list_list_file = open(list_list_path, 'ab')
    for list_row in list_paginator['rows']:
        print 'Querying \'' + list_row['name'] + '\'; id=' + list_row['id'] +' ...'
        list_list =  ac.api('list/list?ids='+list_row['id'])
        json.dump(list_list, list_list_file)
        list_list_file.write('\n')
    list_list_file.close()
    print 'Done!'
    

# ---------------------------------------------------------------------------------------------------------------------
# PRINT

# CAMPAIGN REPORT OPEN LIST
def print_campaign_report_open_lists():
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
        print 'Querying open list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] +' ...'
        campaign_report_open_list = ac.api('campaign/report_open_list?campaignid=' + campaign_row['id'] + '&page=1')
        print json.dumps(campaign_report_open_list)

# CAMPAIGN REPORT LINK LIST    
def print_campaign_report_link_lists():
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
        print 'Querying link list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] + '; messageid='+ str(campaign_row['messageid']) +' ...'
        campaign_report_link_list = ac.api('campaign/report_link_list?campaignid=' + campaign_row['id'] + '&messageid=' + str(campaign_row['messageid']))
        print json.dumps(campaign_report_link_list)

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
        print 'Querying unsubscribe list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id'] +' ...'
        campaign_report_unsubscribe_list = ac.api('campaign/report_unsubscription_list?campaignid=' + campaign_row['id'])
        print json.dumps(campaign_report_unsubscribe_list)

# CAMPAIGN REPORT FORWARD LIST
def print_campaign_report_forward_lists():
    # Paginator is the action that returns a list of campaigns
    print 'Querying campaign paginator ...'
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
        print 'Querying link list for \'' + campaign_row['analytics_campaign_name'] + '\'; id=' + campaign_row['id']  + '; messageid='+ str(campaign_row['messageid']) +' ...'
        campaign_report_forward_list = ac.api('campaign/report_forward_list?campaignid=' + campaign_row['id']+ '&messageid=' + str(campaign_row['messageid']))
        print json.dumps(campaign_report_forward_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Active Campaign')
    parser.add_argument('--mode', type=str, help="Accepted values: 'write' or 'print'")
    parser.add_argument('--info', type=str, help="Accepted values: 'campaigns', 'lists', 'campaign_report_bounce_list'")
    args = parser.parse_args('--mode write --info campaign_report_open_lists'.split()) # parser.parse_args()
    function_name = args.mode + '_' + args.info
    if function_name in dir():
        locals()[function_name]()
    else:
        print 'Argument combination not supported!'


    

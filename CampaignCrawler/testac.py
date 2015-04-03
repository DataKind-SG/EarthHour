from includes.ActiveCampaign import ActiveCampaign
from includes.Config import ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY
import datetime, time

def test_campaign_paginator():
    print 'Testing campaign paginator ...'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    ## 1. tested that hard limit of campaign paginator is 100 campaigns
    ## 2. offset skips campaigns
    ## 3. campaigns['total'] will tell you total number of campaigns available
    ## 4. campaigns['cnt'] returns current count of campaigns returned
    campaigns = ac.api('campaign/paginator?sort=&offset=0&limit=100&filter=0&public=0')
    campaign_rows = campaigns['rows']
    print "rows recorded:" + str(len(campaign_rows))
    if campaigns['total'] > 100:
        outstanding_campaigns = campaigns['total'] - 100
        offset = 100
        print "More than 100 rows detected"
        print "outstanding_campaigns:" + str(outstanding_campaigns)
        print "offset:" + str(offset)
        while outstanding_campaigns > 0:
            campaigns = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=100&filter=0&public=0')
            campaign_rows.extend(campaigns['rows'])
            outstanding_campaigns = outstanding_campaigns - 100
            offset = offset + 100
            print "outstanding_campaigns in loop:" + str(outstanding_campaigns)
            print "offset in loop:" + str(offset)
            print "rows recorded:" + str(len(campaign_rows))
            
def test_open_list_paginator():
    print 'Testing open list paginator'
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    page = 1
    campaign_id = '11'
    open_list_dict = ac.api('campaign/report_open_list?campaignid=' + campaign_id + '&page=' + str(page))
    have_opens = open_list_dict.pop('result_code')
    open_list_dict.pop('result_message')
    open_list_dict.pop('result_output')
    while have_opens == 1:
        print 'page: ' + str(page)        
        open_list_list = list(open_list_dict.values())
        page = page + 1        
        open_list_dict = ac.api('campaign/report_open_list?campaignid=' + campaign_id + '&page=' + str(page))
        have_opens = open_list_dict.pop('result_code')
        open_list_dict.pop('result_message')
        open_list_dict.pop('result_output')
        

if __name__ == '__main__':
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    
    campaigns = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    offset = 0
    campaigns = ac.api('campaign/paginator?sort=&offset='+str(offset)+'&limit=20&filter=0&public=0')
    crows = campaigns['rows']
    
    # documentation points to limit of 20 items per page
    campaign5open = ac.api('campaign/report_open_list?campaignid=11&page=1')
    print ac.api('campaign/report_open_list?campaignid=5&page=1')
    
    campaign11fwd = ac.api('campaign/report_forward_list?campaignid=11&messageid=16')
    campaign5fwdtotal = ac.api('campaign/report_forward_totals?campaignid=5')
    
    campaign5link = ac.api('campaign/report_link_list?campaignid=5&messageid=10')
    
    campaign6unsub = ac.api('campaign/report_unsubscription_list?campaignid=6')
    
    campaign5opentotal = ac.api('campaign/report_open_totals?campaignid=5')
    
    contact = ac.api('contact/view?id=1')
    
    contact_list = ac.api('contact/list?ids=1')
    
    contact_paginator = ac.api('contact/paginator?sort=&offset=0&limit=20&filter=0&public=0')

    ## create contact
#    contact1 = {
#        'email': 'johnsmith@acme.com',
#        'first_name': 'John',
#        'last_name': 'Smith',
#        'p[1]': '1', #p[listid] = listid
#        'status[1]': '1' # status[listid] = 1:active, 2:unsubscribed
#    }    
#    print ac.api('contact/add', contact1)

    ## create campaign code
#    import datetime, time
#    for x in range(0,20):
#        sdate = datetime.datetime.now() + datetime.timedelta(hours = 0, minutes = 2) #scheduled campaign
#        campaign = {
#            'type': 'single',
#            'name': 'testActiveCampaign: %s' % datetime.datetime.now(),
#            'sdate': time.strftime('%Y-%m-%d %H:%M:%S', sdate.timetuple()),
#            'status': 1,
#            'public': 1,
#            'tracklinks': 'all',
#            'trackreads': 1,
#            'htmlunsub': 1,
#            'p[1]': 1, # use list 1 - "gregs"
#            'm[10]': 100 # use message id 10, send to 100% of list
#        }
#        time2 = time.time()
#        print ac.api('campaign/create', campaign)
#        print 'diff2 = %.5f seconds' %(time.time() - time2)
    
    #print ac.api('message/list?ids=10')




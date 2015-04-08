from includes.ActiveCampaign import ActiveCampaign
from includes.Config import ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY
import datetime, time, json

if __name__ == '__main__':
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    
    # campaigns = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    # crows = campaigns['rows']
    
    # documentation points to limit of 20 items per page
    campaign5open = ac.api('campaign/report_open_list?campaignid=92&page=2')
    print json.dumps(campaign5open)
    # print ac.api('campaign/report_open_list?campaignid=5&page=1')
    #
    # campaign11fwd = ac.api('campaign/report_forward_list?campaignid=11&messageid=16')
    # campaign5fwdtotal = ac.api('campaign/report_forward_totals?campaignid=5')
    #
    # campaign5link = ac.api('campaign/report_link_list?campaignid=5&messageid=10')
    #
    # campaign6unsub = ac.api('campaign/report_unsubscription_list?campaignid=6')
    #
    # campaign5opentotal = ac.api('campaign/report_open_totals?campaignid=5')
    #
    # contact = ac.api('contact/view?id=1')
    #
    # contact_list = ac.api('contact/list?ids=5')
    #
    # contact_paginator = ac.api('contact/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    #
    # message_list = ac.api('message/list?ids=all&page=1')
    #
    # message_view = ac.api('message/view?id=10')

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




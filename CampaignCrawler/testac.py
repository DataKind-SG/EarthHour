from includes.ActiveCampaign import ActiveCampaign
from includes.Config import ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY


if __name__ == '__main__':
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)
    
    campaigns = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    crows = campaigns['rows']
    
    print ac.api('campaign/report_open_list?campaignid=5&page=1')
    
    campaign11fwd = ac.api('campaign/report_forward_list?campaignid=11&messageid=16')
    campaign5fwdtotal = ac.api('campaign/report_forward_totals?campaignid=5')
    
    campaign5link = ac.api('campaign/report_link_list?campaignid=5&messageid=10')
    
    campaign6unsub = ac.api('campaign/report_unsubscription_list?campaignid=6')
    
    campaign5opentotal = ac.api('campaign/report_open_totals?campaignid=5')    
    
    #print ac.api('message/list?ids=10')




# -*- coding: utf-8 -*-
"""
Script to pull campaigns

"""

from includes.ActiveCampaign import ActiveCampaign
from includes.Config import ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY

if __name__ == '__main__':
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)

    response =  ac.api('campaign/list?ids=1')
    print response
    
    # Paginator is the action that returns a list of campaigns
    #response = ac.api('campaign/paginator?sort=&offset=0&limit=20&filter=0&public=0')
    
    
    
    

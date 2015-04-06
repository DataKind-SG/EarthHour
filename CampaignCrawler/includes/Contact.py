from Config import ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY
from ActiveCampaign import ActiveCampaign
import json
import urllib2, urllib

class Contact(ActiveCampaign):

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        ActiveCampaign.__init__(self, url, api_key)

    def add(self, params, post_data):
        request_url = '%s&api_action=contact_add&api_output=%s' % (self.url, self.output)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(request_url, post_data)
        response = json.loads(urllib2.urlopen(req).read())
        return response

    def delete(self, params, post_data = {}):
        request_url = '%s&api_action=contact_delete&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response

    def delete_list(self, params, post_data = {}):
        request_url = '%s&api_action=contact_delete_list&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response

    def edit(self, params, post_data):
        request_url = '%s&api_action=contact_edit&api_output=%s' % (self.url, self.output)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(request_url, post_data)
        response = json.loads(urllib2.urlopen(req).read())
        return response

    def note_add(self, params, post_data):
        request_url = '%s&api_action=contact_note_add&api_output=%s' % (self.url, self.output)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(request_url, post_data)
        response = json.loads(urllib2.urlopen(req).read())
        return response

    def note_delete(self, params, post_data = {}):
        request_url = '%s&api_action=contact_note_delete&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response

    def note_edit(self, params, post_data):
        request_url = '%s&api_action=contact_note_edit&api_output=%s' % (self.url, self.output)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(request_url, post_data)
        response = json.loads(urllib2.urlopen(req).read())
        return response
        
    def sync(self, params, post_data):
        request_url = '%s&api_action=contact_sync&api_output=%s' % (self.url, self.output)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(request_url, post_data)
        response = json.loads(urllib2.urlopen(req).read())
        return response

    def tag_add(self, params, post_data):
        request_url = '%s&api_action=contact_tag_add&api_output=%s' % (self.url, self.output)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(request_url, post_data)
        response = json.loads(urllib2.urlopen(req).read())
        return response

    def tag_remove(self, params, post_data):
        request_url = '%s&api_action=contact_tag_remove&api_output=%s' % (self.url, self.output)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(request_url, post_data)
        response = json.loads(urllib2.urlopen(req).read())
        return response

    def list_(self, params, post_data = {}):
        request_url = '%s&api_action=contact_list&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response
        
    def automation_list(self, params, post_data = {}):
        request_url = '%s&api_action=contact_automation_list&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response

    def paginator(self, params, post_data = {}):
        request_url = '%s&api_action=contact_paginator&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response

    def view(self, params, post_data = {}):
        request_url = '%s&api_action=contact_view&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response

    def view_email(self, params, post_data = {}):
        request_url = '%s&api_action=contact_view_email&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response
        
    def view_hash(self, params, post_data = {}):
        request_url = '%s&api_action=contact_view_hash&api_output=%s&%s' % (self.url, self.output, params)
        response = json.loads(urllib2.urlopen(request_url).read())
        return response
    
if __name__ == '__main__':
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)

    ## add
#    contact1 = {
#        'email': 'johnsmith@acme.com',
#        'first_name': 'John',
#        'last_name': 'Smith',
#        'p[1]': '1', #p[listid] = listid
#        'status[1]': '1' # status[listid] = 1:active, 2:unsubscribed
#    }    
#    print ac.api('contact/add', contact1)

    ## delete
    #print ac.api('contact/delete?id=9')

    ## delete list (multiple contacts)
    #print ac.api('contact/delete_list?ids=10,11')

    ## edit
#    contact2 = {
#        'id': 13,
#        'email': 'johnsmith@acme.com',
#        'first_name': 'John Edited',
#        'last_name': 'Smith',
#        'p[1]': '1', #p[listid] = listid
#        'status[1]': '1' # status[listid] = 1:active, 2:unsubscribed
#    }    
#    print ac.api('contact/edit', contact2)

    ## sync
#    contact2 = {
#        'id': 13,
#        'email': 'johnsmith@acme.com',
#        'first_name': 'John Synced',
#        'last_name': 'Smith',
#        'p[1]': '1', #p[listid] = listid
#        'status[1]': '1' # status[listid] = 1:active, 2:unsubscribed
#    }    
#    print ac.api('contact/sync', contact2)

    ## note_add
#    note = {
#        'id': 13, #contact id
#        'listid': 0,
#        'note': 'adding note'
#    }
#    print ac.api('contact/note_add', note)

    ## note delete
    # print ac.api('contact/note_delete?noteid=8') # use 'noteid' instead of 'id'

    ## note_edit
#    note = {
#        'noteid': 5,
#        'id': 13, # refers to contact id. Use 'id' instead of 'subscriberid'
#        'listid': 1,
#        'note': 'editing note 2'
#    }
#    print ac.api('contact/note_edit', note)

    ## tag_add
#    tag = {
#        'id': 13,
#        'tags': 'tags1,tags2,tags3' #add multiple tags delimited by comma
#    }
#    print ac.api('contact/tag_add', tag)

#    ## tag_remove
#    tag = {
#        'id': 13,
#        'tags': 'tags1'
#    }
#    print ac.api('contact/tag_remove', tag)

    ## list
    #print ac.api('contact/list?ids=1')

    ## automation list
    #print ac.api('contact/automation_list?offset=0&limit=20&contact_id=5')

    ## paginator
    #print ac.api('contact/paginator?sort=&offset=0&limit=20&filter=0&public=0')

    ## view
    #print ac.api('contact/view?id=1')

    ## view_email
    #print ac.api('contact/view_email?email=johnsmith@acme.com')

    ## view_hash
    #print ac.api('contact/view_hash?hash=abcdefg1234567')

# Campaign Crawler Readme

## Tested Environment

Python Version: 2.7.8

__Packages Required__
* ActiveCampaign Python API (in ./includes directory)
* json (you may need to install simplejson v3.6.5)
* argparse

## Running the script

Enter the following command in the command line:

`python scraper.py --mode <mode> --info <name of function>`

List of valid modes:
* print
* write

List of valid function names:
* campaigns
* campaign_report_open_lists
* campaign_report_link_lists
* campaign_report_unsubscribe_lists
* campaign_report_forward_lists
* campaign_report_unopen_lists
* lists
* contacts
* message_lists


## References
[Active Campaign API Wrappers](http://www.activecampaign.com/api/wrappers.php)
[Active Campaign Python Library](https://github.com/adulmec/active-campaign-python)

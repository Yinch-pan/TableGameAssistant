import requests
import re
fa_url='https://wiki.biligame.com/'

def get_rolename(ser):
    new_role_patten = re.compile(
        r'<script type="text/javascript">var titles = "(?P<rolename>.*?)";var hasInput = "";</script>', re.S)
    new_resp = requests.get(fa_url+ser+'武将图鉴').text
    # print(new_resp)
    role_names = re.findall(new_role_patten, new_resp)[0].split(',')
    return role_names
a=get_rolename('sgs/')
print(len(a))
def get_single_role(ser,name):
    role_resp=requests.get(fa_url+ser+name).text
    print(role_resp)
get_single_role('sgs/','SP关羽')


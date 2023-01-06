import time
import json
import setting
import requests
import wechatpush
import re

#时间：2022/11/4
#作者：蛋壳
#Another: DanKe
#备注：网易云游戏自动签到

Login_url = setting.LoginUrl
Domain_Status_Url = setting.DomainStatusUrl
Renew_Domain_Url = setting.RenewDomainUrl
token_ptn = re.compile('name="token" value="(.*?)"', re.I)
domain_info_ptn = re.compile(
    r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>',
    re.I)
login_status_ptn = re.compile('<a href="logout.php">Logout</a>', re.I)
sess = requests.Session()
sess.headers.update({
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
})
sess.headers.update({
    'content-type': 'application/x-www-form-urlencoded',
    'referer': 'https://my.freenom.com/clientarea.php'
})
Domain_list = ""
Renew_domains_succeed = ""
Renew_domains_failed = ""

def sign(username,password):#续费
    try:  # 异常捕捉
        r = sess.post(Login_url, data={'username': username, 'password': password})
        if r.status_code != 200:
            print('Can not login. Pls check network.')
            return
        # 查看域名状态
        sess.headers.update({'referer': 'https://my.freenom.com/clientarea.php'})
        r = sess.get(Domain_Status_Url)
    except:
        print('Network failed.')
        return
    # 确认登录状态
    if not re.search(login_status_ptn, r.text):
        print('login failed, retry')
        return
    # 获取token
    page_token = re.search(token_ptn, r.text)
    if not page_token:
        print('page_token missed')
        return
    token = page_token.group(1)
    # 获取域名列表
    domains = re.findall(domain_info_ptn, r.text)
    domains_list = []
    renew_domains_succeed = []
    renew_domains_failed = []
    # 域名续期
    for domain, days, renewal_id in domains:
        days = int(days)
        domains_list.append(f'域名:{domain}还有{days}天到期~')
        if days < 14:
            # 避免频繁操作
            time.sleep(6)
            sess.headers.update({
                'referer':
                f'https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}',
                'content-type': 'application/x-www-form-urlencoded'
            })
            try:
                r = sess.post(Renew_Domain_Url,
                              data={
                                  'token': token,
                                  'renewalid': renewal_id,
                                  f'renewalperiod[{renewal_id}]': '12M',
                                  'paymentmethod': 'credit'
                              })
            except:
                print('Network failed.')
                renew_domains_failed.append(domain)
                continue
            if r.text.find('Order Confirmation') != -1:
                renew_domains_succeed.append(domain)
            else:
                renew_domains_failed.append(domain)
    #print(domains_list, renew_domains_succeed, renew_domains_failed)
    Domain_list = domains_list
    Renew_domains_succeed = renew_domains_succeed
    Renew_domains_failed = renew_domains_failed

def writeMsg(_username,_password):#编辑信息
    sign(_username,_password)
    message = '''⏰当前时间：{} 
尝试为您自动续费Freenom的所有免费域名
####################
您的域名数量：{}
续费失败的域名：{}
续费成功的域名：{}
####################
祝您过上美好的一天！

     ——by DanKe'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),
                        len(Domain_list),
                        Renew_domains_succeed,
                        Renew_domains_failed)
    return message



def handler(event, context):#这里是阿里云的入口，腾讯云要改成main_handler
    config_path = "config.json"
    with open(config_path, "r") as f:
        row_data = json.load(f)
    for user in row_data:
        username = user['username']
        password = user['password']
        pushid = user['pushid']
        try:
            msg = writeMsg(username,password)
        except:
            msg = '签到失败，Authorization可能发生错误'
            msg_en = 'Check in failed,possible error in Authorization'
            print(msg)
            print(msg_en)

        if setting.WechatPush == True :
            wechatpush.push_text(pushid, msg)
        elif setting.WechatPush == False :
            print("微信推送功能未启用")
            print('WeChatPush is not enabled')

if __name__ == '__main__':
    handler(None, None)

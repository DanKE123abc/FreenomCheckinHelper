import time
import json
import setting
import requests
import wechatpush
import re

# 时间：2023/1/8
# 作者：蛋壳
# Another: DanKe
# 备注：Freenom自动续费

Login_url = setting.LoginUrl
Domain_Status_Url = setting.DomainStatusUrl
Renew_Domain_Url = setting.RenewDomainUrl
token_ptn = setting.Token_ptn
domain_info_ptn = setting.Domain_Info_ptn
login_status_ptn = setting.Login_Status_ptn
sess = requests.Session()
sess.headers.update({
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
})
sess.headers.update({
    'content-type': 'application/x-www-form-urlencoded',
    'referer': 'https://my.freenom.com/clientarea.php'
})


def sign(username, password):  # 续费
    try:  # 异常捕捉
        r = sess.post(Login_url, data={
                      'username': username, 'password': password})
        if r.status_code != 200:
            print('Can not login. Pls check network.')
            return False
        # 查看域名状态
        sess.headers.update(
            {'referer': 'https://my.freenom.com/clientarea.php'})
        r = sess.get(Domain_Status_Url)
    except:
        return False
    # 确认登录状态
    if not re.search(login_status_ptn, r.text):
        print('login failed, retry')
        return False
    # 获取token
    page_token = re.search(token_ptn, r.text)
    if not page_token:
        print('page_token missed')
        return False
    token = page_token.group(1)
    # 获取域名列表
    domains = re.findall(domain_info_ptn, r.text)
    domains_list = []
    renew_domains_succeed = []
    renew_domains_failed = []
    # 域名续期
    for domain, days, renewal_id in domains:
        days = int(days)
        domains_list.append(f' {domain}剩余{days}天 ')
        if days < 14:
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
    print(domains_list, renew_domains_succeed, renew_domains_failed)
    result = dict()
    result["list"] = domains_list
    result["succeed_list"] = renew_domains_succeed
    result["failed_list"] = renew_domains_failed
    return result


def writeMsg(_username, _password):  # 编辑信息
    result = sign(_username, _password)
    if result == False:
        sign_result = "失败"
        list = ""
        s_list = ""
        f_list = ""
    else:
        sign_result = "成功"
        list = result["list"]
        s_list = result["succeed_list"]
        f_list = result["failed_list"]
    if len(s_list) > 0 or len(f_list) > 0:
        message = '''⏰当前时间：{} 
尝试为您自动续费Freenom的所有免费域名
####################
🚩登录状态：{}
👓您的域名数量：{}
❌续费失败的域名：{}
✅续费成功的域名：{}
📖域名情况列表：{}
🛃续费成功列表：{}
⛔续费失败列表：{}
####################
祝您过上美好的一天！

         ——by DanKe'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),
                              sign_result,
                              len(list),
                              len(s_list),
                              len(f_list),
                              list,
                              s_list,
                              f_list)
    else:
        message = '''⏰当前时间：{} 
尝试为您自动续费Freenom的所有免费域名
####################
🚩登录状态：{}
👓您的域名数量：{}
❌续费失败的域名：{}
✅续费成功的域名：{}
👀暂无临期域名，列表已隐藏
####################
祝您过上美好的一天！

         ——by DanKe'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),
                              sign_result,
                              len(list),
                              len(s_list),
                              len(f_list))
    return message


def handler(event, context):  # 阿里云，华为云入口
    config_path = "config.json"
    with open(config_path, "r") as f:
        row_data = json.load(f)
    for user in row_data:
        username = user['username']
        password = user['password']
        pushid = user['pushid']
        try:
            msg = writeMsg(username, password)
        except:
            msg = '续费失败，未知错误'
            msg_en = 'Renewal failed, unknown error'
            print(msg)
            print(msg_en)

        if setting.WechatPush == True:
            wechatpush.push_text(pushid, msg)
        elif setting.WechatPush == False:
            print("微信推送功能未启用")
            print('WeChatPush is not enabled')


def main_handler(event, context):  # 腾讯云入口
    handler(event, context)


if __name__ == '__main__':  # 直接运行入口
    handler(None, None)

import re

#--------------------推送设置-----------------------

WechatPush= True
APPID = ""
APPSECRET = ""



#------------------Freenom设置--------------------
LoginUrl = 'https://my.freenom.com/dologin.php'
DomainStatusUrl = 'https://my.freenom.com/domains.php?a=renewals'
RenewDomainUrl = 'https://my.freenom.com/domains.php?submitrenewals=true'
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
Token_ptn = re.compile('name="token" value="(.*?)"', re.I)
Domain_Info_ptn = re.compile(
    r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>',
    re.I)
Login_Status_ptn = re.compile('<a href="logout.php">Logout</a>', re.I)





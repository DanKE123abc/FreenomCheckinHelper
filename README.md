# FreenomCheckinHelper

![Language](https://img.shields.io/badge/Language-Python-yellow)![LICENSE](https://img.shields.io/badge/LICENSE-GPL--3.0-red)![Author](https://img.shields.io/badge/Author-DanKe-blue)

Freenom免费域名自动续费，使用微信订阅号推送信息。

```
            #LICENSE_add
​            该项目附加协议
​               2022/11/4

  在 GPLv3协议（GNU GENERAL PUBLIC LICENSE Version 3）基础上，您需要遵守以下协议：
  （如果本协议与 GPLv3协议 相冲突，请以本协议为准！）

  1.绝对禁止使用本项目进行盈利。
  2.禁止使用本项目名字进行宣传活动。
  3.使用本项目造成的任何后果，该项目所有奉献者与仓库所有者不承担任何法律责任。
  4.当您将本项目代码上传到其他网站向公众发表时，请标注本项目开源地址。
  5.如果本项目侵害到您的权利，请及时联系项目所有者对相关部分进行删除。
  6.如果您使用本项目出现问题时，项目奉献者和仓库所有者有权利不对您进行帮助。
  7.项目所有者有权利对项目内任何部分进行删除。

```

### 注意

新版本中的CheckinHelper已经移除了内置的requests库，需要的请自行安装。

```
pip install requests -t.
```

### 起因

用来自动续费Freenom的免费域名。

参考了网络上的一些其他项目 [参考项目](https://github.com/rpgrpg/freenom-qinglong/blob/main/freenom.py)

### 安装教程

##### 1.登录微信公众平台：[微信公众平台 (qq.com)](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)

​	获得你的微信测试号，在./setting.py里修改`appid`与`appsecret`即可

​	关注你的微信测试号，得到你的推送id（`pushid`）

##### 2.配置信息

​    在./config.json里修改用户信息

​    支持多用户

### 待续

todo

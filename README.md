一个将微信丁香医生的数据(新型冠状病毒 2019-nCoV)部分挪到telegram上，[@dxys_bot](https://t.me/dxys_bot)

### 功能

```
/help - 查看帮助
/overall - 查看概览
/news - 查看最近10条新闻
/rumors - 查看发布的辟谣信息，用法：/rumors 不带参数默认最近5条 或者 /rumors 5/all 带参数获取指定条数
/area - 查看区域统计人数，用法：/area 中国或者/area 全球(只支持国内省，直辖市与自治区)
/sub - 订阅城市/省份统计人数，用法：/sub 广东省或者/sub 广州市(只支持国内省，直辖市与自治区)
/unsub - 取消订阅area - 查看区域统计人数，用法：/area 中国或者/area 全球 或者 /area 广东省(只支持国内省，直辖市与自治区)
```

### 截图

![image.png](https://i.loli.net/2020/02/03/TWG3Ici4xPBZfdC.png)

![image.png](https://i.loli.net/2020/02/03/74IbpLXg5tzOYr9.png)
![image.png](https://i.loli.net/2020/02/03/PoCSWYf8ed9q4LN.png)

### 部署环境

代码基于python3

```
# ubuntu/debian
apt install python3-pip python3 python3-setuptools
pip install -r requirements.txt
```

代码克隆

```
git clone https://github.com/AlphaBrock/dxys
```

修改`config.py`进行配置，TOKEN 为 Bot 的 API

```
TOKEN = 'Your TOKEN'
```

创建单元文件：`vim /lib/systemd/system/dxysbot.service` 自行替换输入如下信息

```
[Unit]	
Description=A Telegram Bot for querying 2019-nCoV
After=network.target network-online.target nss-lookup.target	

[Service]	
Restart=on-failure	
Type=simple	
ExecStart=/usr/bin/python3 /root/dxys/src/main.py	

[Install]	
WantedBy=multi-user.target
```

重新载入 daemon、自启、启动

```
systemctl daemon-reload
systemctl enable dxysbot.service
systemctl start dxysbot.service
```

### THANKS

感谢[DXY-2019-nCoV-Crawler](https://github.com/BlankerL/DXY-2019-nCoV-Crawler)数据提供


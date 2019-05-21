WebSpider
========================

AIKnosearch平台，数据处理引擎，主要功能是对网站的数据进行爬取，以及数据清洗
，将数据存入redis缓存，以及检索引擎elasticsearch中.

Versions
--------
1.0.0

Install
-------
####本地测试
* 搭建虚拟环境(windows) 
    pip install virtualenv //安装虚拟环境管理包
    pip install virtualenvwarpper-win //win下安装virtualenvwapper管理包
    ```
    pip install - i https://pypi.douban.com -r requirements.txt
    ```
    若出现twisted安装异常，打开文件夹req_local安装本地whl包
    ```
    pip install Twisted-19.2.0-cp37-cp37m-win_amd64.whl
    ```
    若出现 No module named 'win32api'
    ```
    pip install -i https://pypi.doubanio.com/simple pypiwin32    
    ```

* Run(本地运行)
 
 将远程服务器地址改为localhost
 
 安装redis服务
 
```
 scrapy crawl bole.py //示例 运行爬虫脚本bole.py
```
    


Deploy
-----
服务器安装scrapyd,scrapyd-client.并部署scrapy项目

编写scrapyd后台启动脚本，搭建后台启动服务

安装第三方scrapy监控服务(如scrapydweb)，实时监控scrapy运行情况
    
     


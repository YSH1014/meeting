## 天文会议系统文档目录

[用例](./doc/Usecase.md)  
[需求](./doc/requirement.md)  
[数据字典](./doc/dataDictionary.md)
[E-R](./doc/ER.md)

### 部署
* 软件环境准备：Python3,pip,postgre数据库
* 安装virtualenv: ```python3 -m pip install virtualenv```
* 建立virtualenv:```python3 -m virtualenv virtualenv```
* 使用virtualenv的python环境：```. virtualenv/bin/activate```
* 安装运行必备包```pip install -r requirements.txt```
* 编写配置文件（新建 .flaskenv 文件)
```
 POSTGRES_URL="xxx.xxx.xxx.xxx:xxxx"
 POSTGRES_USER="xxx"
 POSTGRES_PW="xxx"
 POSTGRES_DB="xxx"

 FLASK_APP=meeting.py
 FLASK_ENV=production
```
* 初始数据库：
```
flask db init
flask db migrate
flask db upgrade
```
* 建立root用户
``` python generate_root.py```
* 运行 ```flask run```
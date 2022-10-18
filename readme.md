# 环境配置和项目启动

## Python和 Anaconda

**1. [安装_Anaconda ](https://anaconda.org.cn/anaconda/install/)**

**2. 进入命令行，执行以下命令，创建anaconda虚拟环境**

   ```powershell
conda env create --name contract_AI --file contract_ai_env.yml
   ```

**3. 配置项目的环境为以上的虚拟环境。**

## MySQL

**1. 本地创建一个数据库，配置如下：**

   ```python
[DATABASE]
port = 3306
user = root
password = root
database = css2
   ```

**2. 执行建表文件：create_db.sql**

## 项目启动和结构

项目入口是main.py，以flask app的形式启动。

**1. Flask Web服务器的目录的说明**，

* 目录app: 有关Flask服务有关的目录

* 目录app/algorithm: 一些简单的算法实现

* 目录app/json_models：有关json处理的模型

* 目录app/models：有关数据库的ORM模型以及DAO函数
* 目录app/static：系统的一些静态文件，包括上传的文件、提供给别人的下载文件、一些内置的文档
* 目录app/temlates: Flask Web前端相关的文件，在前后端分离之后，目前已废弃
* 目录app/tools: 系统抽取的自己编码的一些工具类
* 目录app/views：Flask Web路由函数文件以及路由注册文件

**2. 与合同机器人功能业务有关目录**，

* 目录cont_check：业务与网站分离功能python包，合同合规性审核相关代码
* 目录cont_exam_new：业务与网站分离功能python包，合同对比审核相关代码
* 目录cont_gen：业务与网站分离功能python包，合同生成相关代码
* 目录cont_multi_extract：业务与网站分离功能python包，新版版本多合同要素要素抽取相关代码
* 目录elem_extract：业务与网站分离功能python包，新版版本合同要素要素抽取相关代码
* 目录elem_pickup：业务与网站分离功能python包，旧版本合同要素要素抽取相关代码
* 目录exam_clause：业务与网站分离功能python包，合同条款审核业务功能相关代码
* 目录extends_package：一些离线安装包，以防部署的时候没有安装包

**3. 其他重要的文件**

* config.ini：配置与项目分离，Flask服务器的一些重要配置，包括数据库地址，远程调用吧别的服务接口地址等

* config.py：Flask服务器的配置启动脚本文件

* database_mugration.py：数据库迁移脚本

* install_extends.sh：安装一些扩展包的脚本

* main.py：合同机器人项目运行文件，一般的运行命令为

  ```
  python3 main.py runserver -h 0.0.0.0 -p 5000
  ```

* nginx.conf : nginx负载均衡配置文件

* run_contractai.sh ：通过sh脚本以nginx+uwsgi+flask的方式运行合同机器人项目

* uwsgi.ini： uwsgi服务器运行配置
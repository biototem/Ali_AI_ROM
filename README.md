## 生物图腾关节活动度智能测量康复评定平台demo ##

本demo主要是为了参加阿里云ROM比赛而开设的临时项目，日后开发正式的生物图腾关节活动度智能测量康复评定平台系统时会另起代码仓库。

****

##  运行环境说明 ##

平台的网页前端使用PHP，数据库使用MySQL，后台算法部分是使用python封装阿里云ROM提供的python接口，并且使用fast API进行web端框架提供内部测试和前端接口使用。

其中前端、后端、算法端所需要的软件环境均使用docker进行打包和部署。



## 目录说明 ##

根目录的**script_on_mysql.sql**是创建数据库用户、库表的语句


#### ./docker ####

1. database_built.sh→数据库docker容器的创建语句

2. php_docker_build_run.sh→PHP前端运行环境的docker容器语句，注意需要用到根目录下的**www**(网页脚本)和**nginx**(nginx代理配置脚本)这两个文件夹的文件。

3. simple_det_image_build.sh→

### ./www ###

该目录下存放目前前端所有脚本和相关应用目录。其中目前主要在用的是**./www/upload_demo.php**和**./www/get_result_demo.php**，前者是创建任务上传文件的页面，后者是查看任务结果的页面。

此外需要注意的是，在**./www**目录下有一个名为**Upload**的目录，里面必须有**1**和**2**这两个子目录，而且这几个文件夹必须开放普通用户写入的权限，因为用户上川岛图片最终会通过前端服务存放在该目录中。

#### ./nginx ####
该目录下有**./conf/conf.d/runoob-test-php.conf**文件，内容如下：
```sh
server {
    listen       80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm index.php;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    location ~ \.php$ {
        fastcgi_pass   php:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /www/$fastcgi_script_name;
        include        fastcgi_params;
    }
}
```
-p 8083:80: 端口映射，把 nginx 中的 80 映射到本地的 8083 端口。这样就可以通过docker容器所在机器中的ip+该端口的形式打开前端页面。

#### ./simple_det_image ####

此目录存放算法端所用到的所有脚本和构建docker容器所需要的脚本(详见Dockerfile)

## 运行方法 ##

网页部分已经进行docker部署，浏览器打开http://192.168.3.211:8083/upload_demo.html就可以访问；

如果是非内网环境，访问http://27.45.230.34:8083/upload_demo.html；

此外，我也对上述IP和端口做了内网穿透，用域名访问也可以：http://bio-totem.51vip.biz/upload_demo.html  

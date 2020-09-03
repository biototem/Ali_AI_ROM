#########################################################
# 技巧记录
# 重复技巧，对避免下载失败很有效，例如重复3次：RUN seq 3 | xargs -i apt install LXQT
#########################################################


#########################################################
# base 主要配置CUDA，CUDNN，MINICONDA(PY38)
# 该部分后面可直接用作
#########################################################

FROM ubuntu:focal

# 设定APT源
COPY sources.list /etc/apt/sources.list

# 替换conda源为阿里源
COPY .condarc /root/.condarc

# APT安装基本包
# 需要 perl 安装 cuda
# opencv 需要 libsm0 libglib2.0-bin
RUN export DEBIAN_FRONTEND=noninteractive \
	&& export DEBCONF_NONINTERACTIVE_SEEN=true \
	&& echo 'tzdata tzdata/Areas select Etc' | debconf-set-selections \
	&& echo 'tzdata tzdata/Zones/Etc select UTC' | debconf-set-selections \
	&& apt update \
	&& seq 3 | xargs -i apt install -y  perl gcc g++ make libglu1-mesa-dev libopengl0 libglib2.0-bin libglx-mesa0 sudo vim psmisc ssh net-tools gnupg curl ca-certificates patch git supervisor nginx \
	&& apt clean

# 添加中文支持
RUN apt update \
	&& apt install -y --no-install-recommends language-pack-zh-hans locales fonts-droid-fallback ttf-wqy-zenhei ttf-wqy-microhei fonts-arphic-ukai fonts-arphic-uming fontconfig  \
	&& echo >> /etc/environment \
	&& echo LANG="zh_CN.UTF-8" >> /etc/environment \
	&& echo LANGUAGE="zh_CN:zh:en_US:en" >> /etc/environment \
	&& echo LC_ALL="zh_CN.UTF-8" >> /etc/environment \
	&& echo >> /root/.bashrc \
	&& echo export LANG="zh_CN.UTF-8" >> /root/.bashrc \
	&& echo export LANGUAGE="zh_CN:zh:en_US:en" >> /root/.bashrc \
	&& echo export LC_ALL="zh_CN.UTF-8" >> /root/.bashrc \
	&& locale-gen en_US.UTF-8 \
	&& locale-gen zh_CN.UTF-8 \
	&& locale-gen zh_CN.GBK \
	&& apt clean \
	&& /usr/bin/fc-cache -fv

#########################################################
# extra
#########################################################

ENV BASE_INSTALL=base_install

# 复制待安装文件
COPY $BASE_INSTALL/ /$BASE_INSTALL/

# 安装python
RUN chmod +x -R /$BASE_INSTALL \
	&& /$BASE_INSTALL/Miniconda3-py38_4.8.3-Linux-x86_64.sh -b \
	&& echo \
	&& echo . /root/miniconda3/bin/activate >> /root/.bashrc \
	&& /root/miniconda3/bin/pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
	&& /root/miniconda3/bin/pip install -U pip


#########################################################
# extra2 增加的更多的包
#########################################################

# 安装ffmpeg
RUN apt update \
	&& apt install -y ffmpeg nginx  \
	&& apt clean

# 安装更多python包
COPY det_app /det_app
RUN seq 3 | xargs -i /root/miniconda3/bin/pip install -r /det_app/requirements.txt \
	&& /root/miniconda3/bin/pip uninstall -y pyyaml \
	&& /root/miniconda3/bin/conda install -y pyyaml

# 复制静态网页
COPY web_conf /web_conf
COPY web_root /web_root
COPY ../www/img /web_root
COPY ../www/css /web_root
COPY ../www/js /web_root

#########################################################
# end 保持轻量
#########################################################

# 容器开启时启动
COPY startup.sh /startup.sh
RUN chmod 555 /startup.sh

COPY supervisord_autostart.conf /etc/supervisor/conf.d/

# 入口
CMD ["/startup.sh"]

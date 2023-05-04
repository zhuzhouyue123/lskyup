```shell
 ▄█          ▄████████    ▄█   ▄█▄ ▄██   ▄   ███    █▄     ▄███████▄
███         ███    ███   ███ ▄███▀ ███   ██▄ ███    ███   ███    ███
███         ███    █▀    ███▐██▀   ███▄▄▄███ ███    ███   ███    ███
███         ███         ▄█████▀    ▀▀▀▀▀▀███ ███    ███   ███    ███
███       ▀███████████ ▀▀█████▄    ▄██   ███ ███    ███ ▀█████████▀
███                ███   ███▐██▄   ███   ███ ███    ███   ███
███▌    ▄    ▄█    ███   ███ ▀███▄ ███   ███ ███    ███   ███
█████▄▄██  ▄████████▀    ███   ▀█▀  ▀█████▀  ████████▀   ▄████▀
▀                        ▀
```

# LskyUp

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lskyup?style=for-the-badge)![PyPI - License](https://img.shields.io/pypi/l/lskyup?style=for-the-badge)![GitHub commit activity](https://img.shields.io/github/commit-activity/m/zhuzhouyue123/lskyup?style=for-the-badge)![PyPI](https://img.shields.io/pypi/v/lskyup?style=for-the-badge)![GitHub repo size](https://img.shields.io/github/repo-size/zhuzhouyue123/lskyup?style=for-the-badge)![GitHub top language](https://img.shields.io/github/languages/top/zhuzhouyue123/lskyup?color=orange&style=for-the-badge)![Author: JoeZhu (shields.io)](https://img.shields.io/badge/Author-JoeZhu-green?style=for-the-badge)![Thanks (shields.io)](https://img.shields.io/badge/-Thanks-blue?style=for-the-badge)![for (shields.io)](https://img.shields.io/badge/-for-orange?style=for-the-badge)![visiting (shields.io)](https://img.shields.io/badge/-visiting-success?style=for-the-badge)![my (shields.io)](https://img.shields.io/badge/-my-yellow?style=for-the-badge)![repository (shields.io)](https://img.shields.io/badge/-repository-9cf?style=for-the-badge)![A Star ? (shields.io)](https://img.shields.io/badge/-A%20Star%20%20%3F-yellow?style=for-the-badge)

## 介绍

一个使用Python实现命令行上传图片到LskyPro图床，以及命令行查看LskyPro用户储存情况的小工具

## 目录

* [背景](#背景)
* [原理](#原理)
* [安装](#安装)
* [使用](#使用)
	* [完整命令帮助列表](#完整命令帮助列表)
	* [lskyup config ](#lskyup-config)
	    * [获取token]( #获取token)
	* [lskyup --version](#lskyup---version)
	* [lskyup --info](#lskyup---info)
	* [lskyup --user](#lskyup---user)
	* [lskyup upload](#lskyup-upload)
	    * [lskyup upload --help](#lskyup-upload---help)
	    * [不压缩上传 ](#不压缩上传)
	    * [压缩后上传](#压缩后上传)
* [lskyup clean](#lskyup-clean)
* [Change Log](#Change-Log)
* [LICENSE](#LICENSE)
## 背景

最近在自己的服务器上搭建了一个[LskyPro](https://www.lsky.pro)图床，想配合`Typora`+`Picgo`一起实现博客图片解决方案，但是Picgo现有的插件在我的自建服务上均会报错，所以抽空用Python写了这个命令行程序

## 原理

使用Python的Click库来创建命令行CLI工具

使用Python的requests库来发送GET和POST请求实现上传和参数的返回

使用Python的os、json库来实现路径的获取、拼接和文件的读取写入

图片压缩的算法参考了这个项目[Luban-Py](https://github.com/Freefighter/Luban-Py)

## 安装

使用`pip`包管理工具安装

```shell
pip install lskyup
```

## 使用

### 完整命令帮助列表

```shell
❯ lskyup --help
Usage: lskyup [OPTIONS] COMMAND [ARGS]...

Options:
  -i, --info     Show the current token & server information
  -v, --version  Show the version information
  -u, --user     Show the User information
  --help         Show this message and exit.

Commands:
  clean   Clean Img Cache
  config  Config your server url and api token
  upload  Upload the images
```

### `lskyup config` 

配置Server和Token

```shell
❯ lskyup config
lskyup Copyright (C) 2023-now Joe Zhu
LICENSE GPL-V3
Please enter your Lsky server's url: https://example.com/api/v1
Please enter your own Lsky token: Bearer x|xxxxxxxxxxxxxxxxxxxxxxxxxxx
```

配置文件位于`用户根目录/lskyup/config.json`

#### 获取`token`

```shell
curl -X POST \
-d "email=youremail@example.com&password=yourpassword" \
-H "Accept: application/json" \
https://example.com/api/v1/tokens
```

返回值是`json`格式的，`token`位于`data.token`，格式是`x|xxxxxxxxxxxxxxxxxxxxxx`

token在输入之前请自行加上`Bearer`(注意中间有一个空格)

### `lskyup --version`

输出当前工具版本等信息

```shell
 ▄█          ▄████████    ▄█   ▄█▄ ▄██   ▄   ███    █▄     ▄███████▄
███         ███    ███   ███ ▄███▀ ███   ██▄ ███    ███   ███    ███
███         ███    █▀    ███▐██▀   ███▄▄▄███ ███    ███   ███    ███
███         ███         ▄█████▀    ▀▀▀▀▀▀███ ███    ███   ███    ███
███       ▀███████████ ▀▀█████▄    ▄██   ███ ███    ███ ▀█████████▀
███                ███   ███▐██▄   ███   ███ ███    ███   ███
███▌    ▄    ▄█    ███   ███ ▀███▄ ███   ███ ███    ███   ███
█████▄▄██  ▄████████▀    ███   ▀█▀  ▀█████▀  ████████▀   ▄████▀
▀                        ▀


           Version 0.1.2 © JoeZhu ALL RIGHTS RESERVED
                       LICENSE  GPL-V3
             CONTACT : zhuzhouyue2005@outlook.com
```



### `lskyup --info`

输出当前的配置信息

```shell
❯ lskyup --info
Server: https://example.com/api/v1
Token: Bearer x|xxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### `lskyup --user`

输出当前配置用户的信息

```shell
❯ lskyup --user
USER INFORMATION
User name: Username
E-mail: example@example.com
Website: https://example.com
Image Numbers: 30
Album Numbers: 0
Storage Used/Total: 55122.47 KB/51200000 KB
```

### `lskyup upload`

#### `lskyup upload --help`     

upload子命令帮助列表

```shell
❯ lskyup upload --help
lskyup Copyright (C) 2023-now Joe Zhu
LICENSE GPL-V3
Usage: lskyup upload [OPTIONS] [IMG]...

  Upload the images

Options:
  -c, --compress  Compress your Images before uploading
  --help          Show this message and exit.
```



#### 不压缩上传

`lskyup upload /img1 /img2 /img3`

不压缩上传图片，返回图片访问url，支持多张图片（路径之间一个空格）

```shell
❯ lskyup upload /img1 /img2 /img3 
lskyup Copyright (C) 2023-now Joe Zhu
LICENSE GPL-V3
Uploader is Processing:
Upload uncompressed Img
  [####################################]  100%
Upload Success:
https://example.com/i/2023/05/01/644fsdf6eb1bf.webp
https://example.com/i/2023/05/01/3f4fb1d6eb10d.jpg
https://example.com/i/2023/05/01/a6f4fb12hb15f.png
```

#### 压缩后上传

`lskyup upload -c /img1 /img2 /img3`

压缩后上传图片（增加参数`--compress`）

返回图片访问url，同样支持多张图片（路径之间一个空格）

压缩后的图像缓存在`用户根目录/lskyup/Img_cache`中

```shell
❯ lskyup upload -c /img1 /img2 /img3 
lskyup Copyright (C) 2023-now Joe Zhu
LICENSE GPL-V3
Uploader is Processing:
Upload compressed Img
  [####################################]  100%
Upload Success:
https://example.com/i/2023/05/01/644fsdf6eb1bf.webp
https://example.com/i/2023/05/01/3f4fb1d6eb10d.jpg
https://example.com/i/2023/05/01/a6f4fb12hb15f.png
```

### `lskyup clean`

清理压缩图片缓存（删除`用户根目录/lskyup/Img_cache`文件夹）

```shell
❯ lskyup clean
lskyup Copyright (C) 2023-now Joe Zhu
LICENSE GPL-V3
Clean Img_cache successfully
```

## Change Log
---
### v0.1.4 (2023.5.1 23:01 GMT +8)

- 修复了一些细小的问题

### v0.1.3 (2023.5.1 22:33 GMT +8)

- 更新了README.md
- 修复了一些细小的问题

### v0.1.2 (2023.5.1 21:38 GMT +8)

- 第一个可以用的版本
---

## LICENSE

[GPLv3+](https://github.com/zhuzhouyue123/lskyup/blob/master/LICENSE) © Zhouyue Zhu

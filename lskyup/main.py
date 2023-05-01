import shutil
import click
import requests
import json
from PIL import Image
import os
from shutil import copyfile
from math import ceil


def get_path(types):
    home_dir = os.path.expanduser('~')
    config_dir = os.path.join(home_dir, 'lskyup/')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if types == "config":
        config_file_path = os.path.join(config_dir, "config.json")
        return config_file_path
    elif types == "cache":
        cache_path = os.path.join(config_dir, "Img_cache")
        return cache_path
    elif types == "dir":
        return config_dir


# 这部分代码使用了 Luban-Py 开源项目
# 详见：https://github.com/Freefighter/Luban-Py
#
# 在此保留 Luban-Py 项目的版权声明：
#
# Copyright 2018 Yifan Chen
#
# 本软件源代码受 Apache License, Version 2.0 许可证保护，
# 详见 https://www.apache.org/licenses/LICENSE-2.0.html
#
# 原始代码来自 Luban-Py 项目的 luban.py 文件，我们在此基础上进行了修改和封装。
# 所有权归 Luban-Py 项目作者所有，本代码仅供学习交流使用。


class Compressor(object):  # 压缩器类

    def __init__(self, ignoreBy=102400, quality=75):  # 初始化
        self.img = None
        self.targetPath = None
        self.path = None
        self.type = None
        self.dir = None
        self.filename = None
        self.targetDir = None
        self.ignoreBy = ignoreBy
        self.quality = quality

    def setPath(self, path):
        self.path = path

    def setTargetDir(self, foldername="Img_cache"):

        self.dir, self.filename = os.path.split(self.path)
        self.targetDir = os.path.join(get_path("dir"), foldername)

        if not os.path.exists(self.targetDir):
            os.makedirs(self.targetDir)

        self.targetPath = os.path.join(self.targetDir, "c_" + self.filename)

    def load(self):
        self.img = Image.open(self.path)

        if self.img.mode == "RGB":
            self.type = "JPEG"
        elif self.img.mode == "RGBA":
            self.type = "PNG"
        else:  # 其他的图片就转成JPEG
            self.img = self.img.convert("RGB")
            self.type = "JPEG"

    def computeScale(self):
        # 计算缩小的倍数

        srcWidth, srcHeight = self.img.size

        srcWidth = srcWidth + 1 if srcWidth % 2 == 1 else srcWidth
        srcHeight = srcHeight + 1 if srcHeight % 2 == 1 else srcHeight

        longSide = max(srcWidth, srcHeight)
        shortSide = min(srcWidth, srcHeight)

        scale = shortSide / longSide
        if 1 >= scale > 0.5625:
            if longSide < 1664:
                return 1
            elif longSide < 4990:
                return 2
            elif 4990 < longSide < 10240:
                return 4
            else:
                return max(1, longSide // 1280)

        elif 0.5625 >= scale > 0.5:
            return max(1, longSide // 1280)

        else:
            return ceil(longSide / (1280.0 / scale))

    def compress(self):
        self.setTargetDir()
        # 先调整大小，再调整品质
        if os.path.getsize(self.path) <= self.ignoreBy:
            copyfile(self.path, self.targetPath)

        else:
            self.load()

            scale = self.computeScale()
            srcWidth, srcHeight = self.img.size
            cache = self.img.resize((srcWidth // scale, srcHeight // scale),
                                    Image.ANTIALIAS)

            cache.save(self.targetPath, self.type, quality=self.quality)


def setting(token, url):  # 设置服务器url和Lsky Token，输出到./lskyup/config.json
    user_configs = {"Url": url, "Token": token}
    with open(get_path("config"), "w", encoding="utf-8") as f:
        json.dump(user_configs, f, ensure_ascii=False, indent=4)


def upload_img(url, path, headers):  # 利用request模块，使用POST方式上传图片
    files = {"file": open(path, "rb")}
    if url[-1] == "/" and url[-2] != "/":
        url += "upload"
    else:
        url += "/upload"
    results = requests.post(url, files=files, headers=headers)
    results.encoding = 'utf-8'
    results_data = json.loads(results.text)
    if results.status_code == 200 and (results_data["status"] is True):
        img_url = results_data["data"]["links"]["url"]
        return img_url
    else:
        click.echo("Failed" + str(results.status_code))
        return "fail"


def print_info(ctx, param, value):  # --info 选项的回调函数，显示当前服务信息
    if (not value or ctx.resilient_parsing) and param != "":
        return
    with open(get_path("config")) as config_file:
        settings = json.load(config_file)
    click.echo("Server: " + settings["Url"])
    click.echo("Token: " + settings["Token"])
    ctx.exit()


def print_user_info(ctx, param, value):  # --user 选项的回调函数，显示当前用户信息
    if (not value or ctx.resilient_parsing) and param != "":
        return
    with open(get_path("config")) as config_file:
        settings = json.load(config_file)
    url = settings["Url"] + "/profile"
    token = settings["Token"]
    get_headers = {"Accept": "application/json",
                   "Authorization": token,
                   }
    response = requests.get(url, headers=get_headers)
    response.encoding = 'utf-8'
    response_data = json.loads(response.text)
    if response_data["status"]:
        click.echo(click.style("USER INFORMATION", fg="green", bold=True, italic=True, reverse=True))
        click.echo(click.style("User name: " + response_data["data"]["name"]))
        click.echo(click.style("E-mail: " + response_data["data"]["email"]))
        click.echo(click.style("Website: " + response_data["data"]["url"]))
        click.echo(click.style("Image Numbers: " + str(response_data["data"]["image_num"])))
        click.echo(click.style("Album Numbers: " + str(response_data["data"]["album_num"])))
        click.echo(click.style("Storage Used/Total: "
                               + str(response_data["data"]["used_capacity"])
                               + " KB/"
                               + str(response_data["data"]["capacity"])
                               + " KB"
                               ))
    ctx.exit()


def print_version(ctx, param, value):  # --version 输出版本信息回调函数
    if (not value or ctx.resilient_parsing) and param != "":
        return
    click.secho("""
 ▄█          ▄████████    ▄█   ▄█▄ ▄██   ▄   ███    █▄     ▄███████▄ 
███         ███    ███   ███ ▄███▀ ███   ██▄ ███    ███   ███    ███ 
███         ███    █▀    ███▐██▀   ███▄▄▄███ ███    ███   ███    ███ 
███         ███         ▄█████▀    ▀▀▀▀▀▀███ ███    ███   ███    ███ 
███       ▀███████████ ▀▀█████▄    ▄██   ███ ███    ███ ▀█████████▀  
███                ███   ███▐██▄   ███   ███ ███    ███   ███        
███▌    ▄    ▄█    ███   ███ ▀███▄ ███   ███ ███    ███   ███        
█████▄▄██  ▄████████▀    ███   ▀█▀  ▀█████▀  ████████▀   ▄████▀      
▀                        ▀                                           
    """,
                fg="green"
                )
    click.secho("""
           Version 0.1.4 © JoeZhu ALL RIGHTS RESERVED
                       LICENSE  GPL-V3
             CONTACT : zhuzhouyue2005@outlook.com
    """,
                fg="yellow", bold=True)
    ctx.exit()


@click.group()  # Click命令组
@click.option("-i", "--info",
              is_flag=True,
              callback=print_info,
              expose_value=False,
              is_eager=True,
              help="Show the current token & server information")
@click.option("-v", "--version",
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True,
              help="Show the version information")
@click.option("-u", "--user",
              is_flag=True,
              callback=print_user_info,
              expose_value=False,
              is_eager=True,
              help="Show the User information")
def cli():
    click.echo("lskyup Copyright (C) 2023-now Joe Zhu\nLICENSE GPL-V3")


@cli.command()
def config():  # 设置url和token
    """Config your server url and api token"""
    server_url = click.prompt("Please enter your Lsky server's url")
    user_token = click.prompt("Please enter your own Lsky token")
    setting(user_token, server_url)


@cli.command()
def clean():
    """Clean Img Cache"""
    dir_path = get_path("cache")
    if not os.path.exists(dir_path):
        click.secho("The cache file has already been cleaned", fg="green")
    else:
        try:
            shutil.rmtree(dir_path)
            click.secho("Clean Img_cache successfully", fg="green")
        except OSError as e:
            click.secho(f"{dir_path} ERROR", fg="red")


@cli.command()
@click.option("-c", "--compress",
              is_flag=True,
              help="Compress your Images before uploading")
@click.argument("img", nargs=-1, type=click.Path(exists=True))
def upload(compress, img):  # 上传图片，可以选择是否压缩
    """Upload the images"""
    with open(get_path("config")) as config_file:
        settings = json.load(config_file)
    server_url = settings["Url"]
    img_token = settings["Token"]
    post_headers = {"Accept": "application/json",
                    "Authorization": img_token,
                    }
    click.echo("Uploader is Processing:")
    output = "Upload Success:"
    if compress:
        click.echo("Upload compressed Img")
        compressor = Compressor()
        with click.progressbar(img) as bar:
            for img_path in bar:
                compressor.setPath(img_path)
                compressor.compress()
                result_output = upload_img(server_url, compressor.targetPath, post_headers)
                if result_output == "fail":
                    continue
                else:
                    output += "\n" + result_output
    else:
        click.echo("Upload uncompressed Img")
        with click.progressbar(img) as bar:
            for img_path in bar:
                result_output = upload_img(server_url, img_path, post_headers)
                if result_output == "fail":
                    continue
                else:
                    output += "\n" + result_output
    click.echo(output)


if __name__ == '__main__':
    cli()

import click
import requests
import json
from PIL import Image
import os
from shutil import copyfile
from math import ceil


class Compressor(object):   # 压缩器类

    def __init__(self, ignoreBy=102400, quality=98):  # 初始化
        self.ignoreBy = ignoreBy
        self.quality = quality

    def setPath(self, path):
        self.path = path

    def setTargetDir(self, foldername="Img_cache"):
        self.dir, self.filename = os.path.split(self.path)
        self.targetDir = os.path.join("./LskyProUploader/", foldername)

        if not os.path.exists(self.targetDir):
            os.makedirs(self.targetDir)

        self.targetPath = os.path.join(self.targetDir, "c_"+self.filename)

    def load(self):
        self.img = Image.open(self.path)

        if self.img.mode == "RGB":
            self.type = "JPEG"
        elif self.img.mode == "RGBA":
            self.type = "PNG"
        else:  # 其他的图片就转成JPEG
            self.img == Image.convert("RGB")
            self.type = "JPEG"

    def computeScale(self):
        # 计算缩小的倍数

        srcWidth, srcHeight = self.img.size

        srcWidth = srcWidth + 1 if srcWidth % 2 == 1 else srcWidth
        srcHeight = srcHeight + 1 if srcHeight % 2 == 1 else srcHeight

        longSide = max(srcWidth, srcHeight)
        shortSide = min(srcWidth, srcHeight)

        scale = shortSide / longSide
        if (scale <= 1 and scale > 0.5625):
            if (longSide < 1664):
                return 1
            elif (longSide < 4990):
                return 2
            elif (longSide > 4990 and longSide < 10240):
                return 4
            else:
                return max(1, longSide // 1280)

        elif (scale <= 0.5625 and scale > 0.5):
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
            cache = self.img.resize((srcWidth//scale, srcHeight//scale),
                                    Image.ANTIALIAS)

            cache.save(self.targetPath, self.type, quality=self.quality)


def setting(token, url):  # 设置服务器url和Lsky Token，输出到./LskyProUploader/config.json
    user_configs = {"Url": url, "Token": token}
    with open("./LskyProUploader/config.json", "w", encoding="utf-8") as f:
        json.dump(user_configs, f, ensure_ascii=False, indent=4)


def upload_img(url, path, headers):  # 利用request模块，使用POST方式上传图片
    files = {"file": open(path, "rb")}
    if url[-1] == "/" and url[-2] != "/":
        url+="upload"
    else:
        url+="/upload"
    results = requests.post(url, files=files, headers=headers)
    results.encoding = 'utf-8'
    results_data = json.loads(results.text)
    if results.status_code == 200 and results_data["status"] == True:
        img_url = results_data["data"]["links"]["url"]
        return img_url
    else:
        click.echo("Failed" + str(results.status_code))
        return "fail"
    
def compressor(ctx, param, value, img): # --compress 图片压缩参数回调函数（In Development）
    if (not value or ctx.resilient_parsing) and param != "":
        return
    


def print_info(ctx, param, value):  # --info 选项的回调函数，显示当前服务信息
    if (not value or ctx.resilient_parsing) and param != "":
        return
    with open("./LskyProUploader/config.json") as config_file:
        settings = json.load(config_file)
    click.echo("Server: " + settings["Url"])
    click.echo("Token: " + settings["Token"])
    ctx.exit()


def print_user_info(ctx, param, value):  # --user 选项的回调函数，显示当前用户信息
    if (not value or ctx.resilient_parsing) and param != "":
        return
    with open("./LskyProUploader/config.json") as config_file:
        settings = json.load(config_file)
    url = settings["Url"]+"/profile"
    token = settings["Token"]
    get_headers = {"Accept": "application/json",
                    "Authorization": token,
                    }
    response = requests.get(url,headers=get_headers)
    response.encoding = 'utf-8'
    response_data = json.loads(response.text)
    print(response_data)
    if response_data["status"] == True:
        click.echo(click.style("USER INFORMATION",fg="green",bold=True,italic=True,reverse=True))
        click.echo(click.style("User name: "+response_data["data"]["name"]))
        click.echo(click.style("E-mail: "+response_data["data"]["email"]))
        click.echo(click.style("Website: "+response_data["data"]["url"]))
        click.echo(click.style("Image Numbers: "+str(response_data["data"]["image_num"])))
        click.echo(click.style("Album Numbers: "+str(response_data["data"]["album_num"])))
        click.echo(click.style("Storage Used/Total: "
                   +str(response_data["data"]["used_capacity"])
                   +" KB/"
                   +str(response_data["data"]["capacity"])
                   +" KB"
                   ))
    ctx.exit()

def print_version(ctx, param, value):   # --version 输出版本信息回调函数
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
           Version 0.1 © JoeZhu ALL RIGHTS RESERVED
                       LICENSE  GPL-V3
             CONTACT : zhuzhouyue2005@outlook.com
    """,
    fg="yellow",bold=True)
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
    click.echo("Thanks to use LskyProUploader!")  #


@cli.command()
def config():  # 设置url和token
    """Config your server url and api token"""
    server_url = click.prompt("Please enter your Lsky server's url")
    user_token = click.prompt("Please enter your own Lsky token")
    setting(user_token, server_url)


@cli.command()
@click.option("-c", "--compress",
              is_flag=True,
              expose_value=False,
              is_eager=True,
              help="Compress your Images before uploading")
@click.argument("img", nargs=-1, type=click.Path(exists=True))
@click.pass_context
def upload(compress,img):  # 上传图片
    """Upload the images"""
    if compress:
        compressor = Compressor()
        with open("./LskyProUploader/config.json") as config_file:
            settings = json.load(config_file)
        server_url = settings["Url"]
        img_token = settings["Token"]
        post_headers = {"Accept": "application/json",
                        "Authorization": img_token,
                        }
        click.echo("Uploader Processing:")
        output = "Upload Success:"
        with click.progressbar(img) as bar:
            for img_path in bar:
                compressor.setPath(img_path)
                compressor.compress()
                result_output = upload_img(server_url, compressor.targetPath, post_headers)
                if result_output == "fail":
                    continue
                else:
                    output += "\n" + result_output
        click.echo(output)
    else:
        with open("./LskyProUploader/config.json") as config_file:
            settings = json.load(config_file)
        server_url = settings["Url"]
        img_token = settings["Token"]
        post_headers = {"Accept": "application/json",
                        "Authorization": img_token,
                        }
        click.echo("Uploader Processing:")
        output = "Upload Success:"
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

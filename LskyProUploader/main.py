import click
import requests
import json


def setting(token, url):  # 设置服务器url和Lsky Token，输出到LskyProUploader/config.json
    user_configs = {"Url": url, "Token": token}
    with open("LskyProUploader/config.json", "w", encoding="utf-8") as f:
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
    
def compressor(ctx, param, value): # --compress 图片压缩参数回调函数（In Development）
    if (not value or ctx.resilient_parsing) and param != "":
        return
    print(param)
    ctx.exit()


def print_info(ctx, param, value):  # --info 选项的回调函数，显示当前服务信息
    if (not value or ctx.resilient_parsing) and param != "":
        return
    with open("LskyProUploader/config.json") as config_file:
        settings = json.load(config_file)
    click.echo("Server: " + settings["Url"])
    click.echo("Token: " + settings["Token"])
    ctx.exit()


def print_user_info(ctx, param, value):  # --user 选项的回调函数，显示当前用户信息
    if (not value or ctx.resilient_parsing) and param != "":
        return
    with open("LskyProUploader/config.json") as config_file:
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

def print_version(ctx, param, value):
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
              callback=compressor,
              expose_value=False,
              is_eager=True,
              help="Compress your Images before uploading")
@click.argument("img", nargs=-1, type=click.Path(exists=True))
def upload(img):  # 上传图片
    """Upload the images"""
    with open("LskyProUploader/config.json") as config_file:
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

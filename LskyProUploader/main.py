import click
import requests
import json


def setting(token, url):  # 设置服务器url和Lsky Token，输出到config.json
    user_configs = {"Url": url, "Token": token}
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(user_configs, f, ensure_ascii=False, indent=4)


def upload_img(url, path, headers):  # 利用request模块，使用POST方式上传图片
    files = {"file": open(path, "rb")}
    results = requests.post(url, files=files, headers=headers)
    results.encoding = 'utf-8'
    if results.status_code == 200:
        results_data = json.loads(results.text)
        img_url = results_data["data"]["links"]["url"]
        click.echo(img_url)
    else:
        results.raise_for_status()


def print_info(ctx, param, value):  # param 为选项变量 click.Option
    if (not value or ctx.resilient_parsing) and param != "":
        return
    with open("config.json") as config_file:
        settings = json.load(config_file)
    click.echo("Server: "+settings["Url"])
    click.echo("Token: "+settings["Token"])
    ctx.exit()


@click.group()  # Click命令组
@click.option("-i", "--info",
              is_flag=True,
              callback=print_info,
              expose_value=False,
              is_eager=True,
              help="Show the current token & server")
def cli():
    click.echo("Thanks to use LskyProUploader!")  # 感谢使用本工具


@cli.command()
def config():  # 设置url和token
    """Config the api token and server url"""
    user_token = click.prompt("Please enter your own Lsky token")
    server_url = click.prompt("Please enter your Lsky server's url")
    setting(user_token, server_url)


@cli.command()
@click.argument("img", nargs=-1, type=click.Path(exists=True))
def upload(img):  # 上传图片
    """Upload the img"""
    with open("config.json") as config_file:
        settings = json.load(config_file)
    server_url = settings["Url"]
    img_token = settings["Token"]
    post_headers = {"Accept": "application/json",
                    "Authorization": img_token,
                    }
    click.echo("Upload Success:")
    for img_path in img:
        upload_img(server_url, img_path, post_headers)


if __name__ == '__main__':
    cli()

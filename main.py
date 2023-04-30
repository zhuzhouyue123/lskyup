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


@click.group()  # Click命令组
def main():
    click.echo("Thanks to use LskyProUploader!")  # 感谢使用本工具


@main.command()
def config():  # 设置url和token
    user_token = click.prompt("Please enter your own Lsky token")
    server_url = click.prompt("Please enter your Lsky server's url")
    setting(user_token, server_url)


@main.command()
@click.argument("img", nargs=-1, type=click.Path(exists=True))
def upload(img):  # 上传图片
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
    main()

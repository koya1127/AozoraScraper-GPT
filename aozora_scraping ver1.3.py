import requests
from bs4 import BeautifulSoup
import os

def fetch_html(url):
    response = requests.get(url)
    return response.content

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text_parts = soup.find_all("div", class_="main_text")
    return "\n".join([part.get_text() for part in text_parts])

#return が実行された時点で、その関数の処理は終了
def validate_file_path():
    while True:
        file_path = input("保存するファイルのパスを入力してください。...")
        if os.path.isdir(file_path):
            print("ディレクトリだけではなく、ファイル名も入力してください！")
        elif os.path.exists(os.path.dirname(file_path)) or os.path.dirname(file_path) == '':
            return file_path
        else:
            print("指定されたディレクトリが存在しません。もう一度確認してください。")

def save_text_to_file(file_path, text):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
    print("データ収集完了")

# メインの処理
def main():
    url = "https://www.aozora.gr.jp/cards/000148/files/773_14560.html"
    html_content = fetch_html(url)
    text = extract_text_from_html(html_content)
    file_path = validate_file_path()
    save_text_to_file(file_path, text)

# プログラムのエントリーポイント
if __name__ == "__main__":
    main()
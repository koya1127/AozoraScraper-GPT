import requests
from bs4 import BeautifulSoup
import os

# 青空文庫の作品ページのURL（ここでは『こころ』の例）
url = "https://www.aozora.gr.jp/cards/000148/files/773_14560.html"

# URLにアクセスしてHTMLデータを取得
response = requests.get(url)

# BeautifulSoupを使ってHTMLを解析
soup = BeautifulSoup(response.content, "html.parser")

# 青空文庫の作品テキストが含まれる部分を抽出、find_allは指定した条件に一致するすべてのHTML要素をリスト形式で返す。class_="main_text"がhtml中に二つあったら二要素のリストを返す。
text_parts = soup.find_all("div", class_="main_text")

# テキスト部分を結合して一つの文字列にまとめる、get_textはBeautifulSoupのメソッドでHTML要素内のテキストを全て返す。<ruby> タグ内のテキスト（ふりがな部分も含めて）もすべて取り出される。
text = "\n".join([part.get_text() for part in text_parts])

# ユーザーに保存先のファイルパスを尋ねる
file_path = input("保存するファイルのパスを入力してください。kokoro.txtと入力するとカレントディレクトリに保存されます。 C:/Users/YourName/Documents/kokoro.txtみたいにパスを渡す際はファイル名の記入を忘れずに！ ")

#os.path.isdir(file_path)は、file_path がディレクトリであるかどうかを確認する関数で、True or Falseを返す。
if os.path.isdir(file_path):
    print("ディレクトリだけじゃなくファイル名を入力してね！")

# 結果をファイルに保存、open関数は、「既存のファイルを開く」もしくは「新しいファイルを作成して開く」という二つの機能を持っている。Pythonのopen 関数は、ファイルパスとファイル名がセットで提供されることが前提。そのため、ファイル名が含まれていないと、どのファイルを開くか（または作成するか）を判断できず、エラーとなります。
with open(file_path, "w", encoding="utf-8") as file:
    file.write(text)

print("データ収集完了")
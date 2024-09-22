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

# テキスト部分を結合して一つの文字列にまとめる、get_textはBeautifulSoupのメソッドでHTML要素内のテキストを全て返す。<ruby> タグ内のテキスト（ふりがな部分も含めて）もすべて取り出される。\nは改行、"\n".joinでリスト内の要素を改行してくっつける。
text = "\n".join([part.get_text() for part in text_parts])

# ユーザーに保存先のファイルパスを尋ねる、while True:はwhileの横の条件がtrueになる限りループし続ける。今回はbreakしない限り常にTrue。
while True:
    file_path = input("保存するファイルのパスを入力してください。kokoro.txtと入力するとカレントディレクトリに保存されます。C:/Users/YourName/Documents/kokoro.txtみたいにパスを渡す際はファイル名の記入を忘れずに！ ")

    # ディレクトリのみの場合、#os.path.isdir(file_path)は、file_path が「存在する」ディレクトリであるかどうかを確認する関数で、True or Falseを返す。
    if os.path.isdir(file_path):
        print("ディレクトリだけではなく、ファイル名も入力してください！例：C:/Users/YourName/Documents/kokoro.txt")
    # ファイル名が正しく入力されている場合。os.path.dirname(file_path)は、ユーザーが入力した file_path からディレクトリ部分（ファイル名を除いたパス）を取り出す。os.path.exists() 関数は、指定されたディレクトリが実際に存在するかどうかを確認する。os.path.dirname(file_path) == ''はユーザーがファイル名だけを指定した場合でも、コードが問題なく進行するようにしている。
    elif os.path.exists(os.path.dirname(file_path)) or os.path.dirname(file_path) == '':
        break
    # 存在しないディレクトリが入力された場合
    else:
        print("指定されたディレクトリが存在しません。もう一度確認してください。")

# 結果をファイルに保存、open関数は、「既存のファイルを開く」もしくは「新しいファイルを作成して開く」という二つの機能を持っている。Pythonのopen 関数は、ファイルパスとファイル名がセットで提供されることが前提。そのため、ファイル名が含まれていないと、どのファイルを開くか（または作成するか）を判断できず、エラーとなる。open関数はフルパスだとその場所を参照、ファイル名のみだと、カレントディレクトリを参照。"w" は書き込みモードを意味し、指定したファイルが既に存在していればその内容を上書きし、新しいファイルを作成する場合は新規作成します。encoding="utf-8": ファイルをUTF-8という文字コードで保存します。日本語などの文字を正しく扱うために、このエンコーディング指定が必要です。as fileはwithの中でのみ動作する変数を定義。with は、「リソースを使い終わったら必ず片付けてくれるお手伝いさん」
with open(file_path, "w", encoding="utf-8") as file:
    file.write(text)

print("データ収集完了")
import requests
from bs4 import BeautifulSoup
import os

# 著者ページからすべての作品URLを取得
def fetch_author_works(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.content, "html.parser")
    works = []
    # 著者の作品リストのリンクを取得（リンク先が著者ページにより異なるため調整が必要）、BeautifulSoupで、ページ内のすべての<a>タグ（リンク）を取得する。その後、各<a>タグからhref属性を取り出しています。
    for link in soup.find_all("a"):
        url = link.get("href")
        if url and "cards" in url:  # 作品ページリンクをフィルタリング、if urlはurlという変数に何か入っていたらtrue、そうでないならfalse。fは、文字列の中に変数の値や式を簡単に埋め込むための書き方で、fの後に続く文字列の中で、中括弧 {} を使って変数を埋め込むことができます。
            works.append(f"https://www.aozora.gr.jp{url}")
    return works

# 作品のテキストを取得
def fetch_html(url):
    response = requests.get(url)
    return response.content

# テキストを抽出
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text_parts = soup.find_all("div", class_="main_text")
    return "\n".join([part.get_text() for part in text_parts])

# 自動的にファイルを保存する
def save_text_to_file(file_path, text):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"保存完了: {file_path}")

# メインの処理
def main():
    author_url = "https://www.aozora.gr.jp/index_pages/person148.html"  # 著者ページのURL
    works = fetch_author_works(author_url)
    
    save_directory = "作品保存ディレクトリ"  # 保存先ディレクトリを指定
    
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    for work_url in works:
        html_content = fetch_html(work_url)
        text = extract_text_from_html(html_content)
        
        # 作品名を抽出（作品名のタグがある場所を取得）
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.find("h1").get_text()  # タイトルを取得
        
        # 自動的にファイル名を設定
        file_path = os.path.join(save_directory, f"{title}.txt")
        save_text_to_file(file_path, text)

if __name__ == "__main__":
    main()

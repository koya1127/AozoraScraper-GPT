青空文庫スクレイパー

このPythonスクリプトは、青空文庫に掲載されている作品からテキストをスクレイピングし、テキストファイルとして保存します。

## 機能

- **HTMLコンテンツの取得**: 指定された青空文庫のURLからHTMLコンテンツを取得します。
- **テキストの抽出**: HTMLコンテンツを解析し、作品のメインテキストを抽出します。
- **テキストのファイル保存**: 抽出したテキストを指定されたファイルパスに保存します。

## 必要要件

- Python 3.x
- `requests`ライブラリ
- `BeautifulSoup` (`bs4`パッケージの一部)

## 使い方

1. スクリプトのURL部分を、解析したい青空文庫作品のURLに変更します。
2. スクリプトを実行します。
3. 保存するファイルのパスを入力すると、指定された場所にテキストファイルが保存されます。


## スクリプトの構成

- `fetch_html(url)`: 指定されたURLからHTMLコンテンツを取得します。
- `extract_text_from_html(html_content)`: 取得したHTMLコンテンツからテキスト部分を抽出します。
- `validate_file_path()`: ユーザーにファイルパスを入力させ、存在するディレクトリを確認します。
- `save_text_to_file(file_path, text)`: 抽出されたテキストを指定されたファイルパスに保存します。
- `main()`: スクリプトのメイン処理を実行します。

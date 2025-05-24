import os
import requests
from bs4 import BeautifulSoup


def fetch_html(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def extract_text_from_html(html_content: bytes | str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    text_parts = soup.find_all("div", class_="main_text")
    return "\n".join(part.get_text() for part in text_parts)


def fetch_author_works(author_url: str) -> list[str]:
    response = requests.get(author_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    works = []
    for link in soup.find_all("a"):
        url = link.get("href")
        if url and "cards" in url:
            works.append(f"https://www.aozora.gr.jp{url}")
    return works


def save_text_to_file(file_path: str | os.PathLike, text: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


def main() -> None:
    author_url = "https://www.aozora.gr.jp/index_pages/person148.html"
    works = fetch_author_works(author_url)
    save_directory = "作品保存ディレクトリ"
    os.makedirs(save_directory, exist_ok=True)
    for work_url in works:
        html_content = fetch_html(work_url)
        text = extract_text_from_html(html_content)
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.find("h1").get_text()
        file_path = os.path.join(save_directory, f"{title}.txt")
        save_text_to_file(file_path, text)


if __name__ == "__main__":
    main()

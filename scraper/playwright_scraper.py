from playwright.sync_api import sync_playwright
import os
from datetime import datetime


def scrape_chapter(url: str, output_dir: str) -> str:
    """
    Scrapes text content and full-page screenshot from the given Wikisource URL.

    Args:
        url (str): URL of the chapter page.
        output_dir (str): Directory to save outputs.

    Returns:
        str: Path to the saved raw text file.
    """
    os.makedirs(os.path.join(output_dir, "screenshots"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "raw"), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")

        # Take screenshot
        screenshot_path = os.path.join(output_dir, "screenshots", f"chapter_screenshot_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
        page.screenshot(path=screenshot_path, full_page=True)

        # Scrape main text content
        content = page.locator("#mw-content-text").inner_text()
        text_path = os.path.join(output_dir, "raw", "latest_chapter.txt")

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(content)

        browser.close()

    return text_path


if __name__ == "__main__":
    chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    output_directory = "../data"
    saved_path = scrape_chapter(chapter_url, output_directory)
    print(f"Chapter content saved at: {saved_path}")

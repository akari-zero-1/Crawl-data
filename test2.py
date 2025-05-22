from playwright.sync_api import sync_playwright
import time
import random
import json
import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/render/project/.playwright"



def explore_tiktok_scroll_and_collect():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0"})

        page.goto("https://www.tiktok.com/explore")
        time.sleep(5)

        video_urls = set()
        collected = 0
        round_counter = 0

        try:
            while collected < 60:
                print(f"\nRound {round_counter + 1}...")
                links = page.query_selector_all("a")

                for link in links:
                    href = link.get_attribute("href")
                    if href and "/video/" in href and href not in video_urls:
                        video_urls.add(href)
                        print(f"Video: {href}")
                        collected += 1
                        if collected % 6 == 0:
                            a = random.randint(1, 10)
                            print(f"\nStop {a} seconds")
                            time.sleep(a)
                        if collected >= 60:
                            break

                # Scroll xuống 1000 px
                page.evaluate("window.scrollBy(0, 1000);")
                time.sleep(random.randint(1, 5))
                round_counter += 1

        except Exception as e:
            print("ERROR:", e)

        print("\n Total URL video:")
        for url in video_urls:
            print(url)
        print(f"\n Total amount video: {len(video_urls)}")

        output_data = {
            'video_url': list(video_urls),
        }

        with open("video_url.json", 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
            print("Save file video_url.json!")


if __name__ == "__main__":
    explore_tiktok_scroll_and_collect()

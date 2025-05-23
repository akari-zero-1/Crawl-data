import json
from pymongo import MongoClient
from datetime import datetime, timezone


def run():
    client = MongoClient("mongodb://localhost:27017")
    db = client["tiktok_data"]
    collection = db["video_urls"]

    try:
        with open("video_url.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File video_url.json không tồn tại!")
        return
    except json.JSONDecodeError:
        print("File video_url.json không đúng định dạng JSON!")
        return

    url_list = data.get("video_url", [])
    if not url_list:
        print("Không có URL nào trong file.")
        return

    for url in url_list:
        video_id = url.split("/")[-1]
        author = url.split("/")[-3]

        doc = {
            "url": url,
            "video_id": video_id,
            "author": author,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        collection.update_one(
            {"video_id": video_id},
            {"$setOnInsert": doc},
            upsert=True
        )

    print("OK!")


if __name__ == "__main__":
    run()

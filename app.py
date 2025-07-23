import os
from fastapi import FastAPI
from notion_client import Client
import openai

app = FastAPI()

# Renderでは環境変数管理なのでdotenvは不要
notion = Client(auth=os.environ["NOTION_API_KEY"])
openai.api_key = os.environ["OPENAI_API_KEY"]
DATABASE_ID = os.environ["DATABASE_ID"]
PARENT_PAGE_ID = os.environ["PARENT_PAGE_ID"]  # 新規ページ親（どこに作るか）

@app.post("/rewrite")
def rewrite_one():
    # 1. Notionから元記事を1件取得
    response = notion.databases.query(database_id=DATABASE_ID, page_size=1)
    original_page = response["results"][0]
    ORIGINAL_PAGE_ID = original_page["id"]

    # 2. 元記事本文の取得（段落のみ/必要に応じカスタマイズ）
    blocks = notion.blocks.children.list(ORIGINAL_PAGE_ID)
    original_content = ""
    for block in blocks["results"]:
        if block["type"] == "paragraph":
            texts = block["paragraph"]["rich_text"]
            if texts:
                original_content += "".join([t["plain_text"] for t in texts]) + "\n"

    # 3. GPTでリライト
    prompt = f"以下の文章を、初心者にも分かりやすく丁寧な日本語でリライトしてください。\n\n{original_content}"
    response_gpt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはSEOに強い日本語Webライターです。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    rewrite_text = response_gpt["choices"][0]["message"]["content"]

    # 4. Notionに新規ページ作成
    REWRITE_TITLE = "【リライト】" + original_page["properties"]["Name"]["title"][0]["plain_text"]
    new_page = notion.pages.create(
        parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
        properties={
            "title": [{
                "type": "text",
                "text": {"content": REWRITE_TITLE}
            }]
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": rewrite_text
                            }
                        }
                    ]
                }
            }
        ]
    )

    # 5. 新ページのURLを元記事に登録
    new_page_url = new_page["url"]
    notion.pages.update(
        page_id=ORIGINAL_PAGE_ID,
        properties={
            "リライト案URL": {"url": new_page_url}
        }
    )
    return {"result": "OK", "url": new_page_url}

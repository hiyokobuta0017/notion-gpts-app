# Notion × GPTs FastAPI テンプレート

このテンプレートは、Notion APIとGPTsを連携するためのFastAPIアプリの最小構成です。

## 起動方法（Render用）

- Build Command:
  ```
  pip install -r requirements.txt
  ```

- Start Command:
  ```
  uvicorn main:app --host 0.0.0.0 --port 10000
  ```

## 環境変数

- NOTION_TOKEN
- DATABASE_ID

これらはNotion連携で必要になります。

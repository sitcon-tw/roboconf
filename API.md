staff.sitcon.org API
===
使用 API 時皆需以 POST 方式呼叫，否則會看到可愛的[400](http://staff.sitcon.org/400)頁面喔。目前設計的通則如下：

* 連接端點：/[應用程式名稱]/api
* 對應程式碼：/[appname]/api.py
* 參數：
  - `action`: 每個 API call 都必須包含此參數，指明要使用的功能。
* 傳回結果：
  - HTTP 200: API call 有效時，必定傳回一`application/json`，內容隨 API 而異。
  - HTTP 400: 當沒有符合的 API `action`，或是使用 HTTP GET 時觸發。傳回錯誤網頁。

工作人員資訊
---
端點：/users/api

* `get`
  - 參數：`username`
  - 當使用者不存在或無效，傳回 `{"status": "invalid"}`
  - 當使用者存在，傳回：
    ```
    {
        "status": "success",
        "name": "RSChiang",
        "title": "行政組長",
        "avatar": "https://secure.gravatar.com/..."
    }
    ```
* `list`
  - 列出工作人員。
  - 傳回以下陣列：
    ```
    {
        "denny0223": {
            "title": "總召",
            "avatar": "https://secure.gravatar.com/..."
        },

        "RSChiang": {
            "title": "行政組長",
            "avatar": "https://secure.gravatar.com/..."
        },

        "elct9620": {
            "title": "文創煉金師",
            "avatar": "https://secure.gravatar.com/..."
        },
    }
    ```

議題追蹤系統 (issue tracker)
---
（建構中）

文件系統
---
（建構中）

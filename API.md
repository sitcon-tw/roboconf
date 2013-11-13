staff.sitcon.org API
===

工作人員資訊
---
端點：/users/api

### GET
列出工作人員，回傳如下結果：
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

#### (`name`)
取得特定工作人員資訊。  
當使用者不存在或無效，傳回 **HTTP 400** `{"status": "invalid"}`。

回傳如下結果：
```
{
    "status": "success",
    "name": "RSChiang",
    "title": "行政組長",
    "avatar": "https://secure.gravatar.com/..."
}
```

文件系統
---
端點：/docs/api

* 當存取的物件不存在，傳回 **HTTP 400** `{"status": "invalid_property"}`。  
* 當不具物件的相對應權限，傳回 **HTTP 403** `{"status": "permission_denied"}`。
* 成功時傳回 `{"status": "success"}`。  

### GET

#### (`nid`)
取得文件或資料夾節點資訊，物件皆以節點ID (nid) 識別。

接受額外參數 `details`，可以以 JSON 陣列指定要取得的各部分資訊：

* `node`: 預設。名稱、上次修改時間等節點資訊。
* `content`: 檔案或資料夾內容。
* `revisions`: 檔案修訂記錄。

資料夾回傳如下結果：
```
{
  "status": "success",
  "name": "會議記錄",
  "content": ["MTZE", "MkY", "MjZG", "MzE2Rg"],
  "parent": "MkQ",
  "modified": "2013-11-13T13:10:00.160933",
  "archived": false,
  "starred": false,
}
```

檔案傳回如下結果：
```
{
  "status": "success",
  "name": "SITCON 2014 企劃書",
  "revision": 16,
  "author": "RSChiang",
  "content": "SITCON 2014 企劃書\n===\n## 一、...",
  "format": "markdown",
  "parent": "MkQ",
  "modified": "2013-11-13T19:23:06.235766",
  "archived": false,
  "starred": false,
}
```

### POST

#### (`nid`, `content`)
更新文件檔案，建立新修訂版本。

接受以下額外參數：

* `type`: 內容類型。預設為純文字，接受 `markdown`, `text`, `html`。
* `comment`: 修訂版本的敘述。
* 將 `type` 指定為 `link`，可以更新外部連結文件的網址，或是將伺服器本地文件轉換為外部文件。反之亦然。

傳回如下結果：
```
{
  "status": "success",
  "base": 16,
  "current": 17,
  "timestamp": "2013-11-13T20:38:05.625765",
}
```

### PUT

參數以 JSON 傳入。

#### (`nid`, `action`)
對文件或資料夾節點進行操作。

* `star`/`unstar`：加上或取消星號標記。
* `rename`：重新命名物件。
* `move`：將物件移動到新的資料夾。
* `delete`：將物件移到垃圾桶。
* `archive`：封存檔案或資料夾，防止任何人修改，只允許擁有封存權限的人移動、刪除。

#### (`nid`, `permissions`)
覆寫節點權限。

`permissions` 需為 JSON 格式陣列，每一項目包含：

* 權限套用的範圍，擇一
    - `scope`: 特定身分。接受公開 (`*`)、工作人員 (`staff`)、系統管理者 (`admin`)
    - `user`: 特定的使用者名稱
    - `group`: 特定的群組名稱
* `type`: 權限種類，接受 `view`, `comment`, `edit`。
* `effect`: 權限效果，可以是允許 (`allow`) 或是拒絕 (`deny`)。

議題追蹤系統 (issue tracker)
---
（建構中）

staff.sitcon.org API
===

總則
---
* API 皆與普通界面共用資源端點，因此須於標頭指定 `X-Requested-With` 方能正常存取。  
* PUT 與 DELETE 方法皆以 JSON 傳入參數。
* 當存取的物件不存在，傳回 **HTTP 404**。
* 當不具物件的相對應權限，傳回 **HTTP 403**。
* 尚未實作的 API 功能，傳回 **HTTP 501**。
* 成功時必定會傳回參數 `{"status": "success"}`。

工作人員資訊
---
### /users/

#### GET

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

### /users/`username`

#### GET

取得特定工作人員資訊。  
當使用者帳號無法使用，傳回 **HTTP 400** `{"status": "invalid"}`。

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
物件皆以節點ID (nid) 識別。

### /docs/new

#### POST

建立新文件或資料夾。

* `type`: `file` 或是 `folder`。
* `name`: 節點名稱。
* `at`: 上層資料夾的節點ID。
* 如果為檔案，接受所有針對檔案內容更新之操作。見 /docs/`nid`/ (POST)。

回傳如下結果：
```
{
  "status": "success",
  "nid": "MjZG",
  "timestamp": "2013-11-13T19:23:06.235766"
}
```

檔案會額外回傳如下資訊：
```
{
  ...
  "revision": 16,
  ...
}
```

### /docs/`nid`

#### GET

接受額外參數 `details`，可以指定要取得的各部分資訊：

* `node`: 預設。名稱、上次修改時間等節點資訊。
* `content`: 檔案或資料夾內容。
* `revisions`: 檔案修訂記錄。

回傳如下結果：
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

檔案會額外傳回如下資訊：
```
{
  ...
  "revision": 16,
  "author": "RSChiang",
  "content": "SITCON 2014 企劃書\n===\n## 一、...",
  "format": "markdown",
  ...
}
```

#### POST

更新文件檔案，建立新修訂版本。

接受以下參數：

* `content`: 檔案內容。
* `format`: 內容類型。預設為純文字，接受 `markdown`, `text`, `html`。
* `comment`: 修訂版本的敘述。
* 將 `format` 指定為 `link`，可以更新外部連結文件的網址，或是將伺服器本地文件轉換為外部文件。反之亦然。

傳回如下結果：
```
{
  "status": "success",
  "base": 16,
  "current": 17,
  "timestamp": "2013-11-13T20:38:05.625765",
}
```

#### PUT

對文件或資料夾節點進行操作，接受以下任一參數：

* `star`/`unstar`：加上或取消星號標記。
* `rename`：重新命名物件，值為。
* `move`：將物件移動到另外的資料夾。
* `archive`/`unarchive`：封存檔案或資料夾，防止任何人修改，只允許擁有封存權限的人移動、刪除。
* `permissions`: 覆寫節點權限。

`permissions` 需為 JSON 格式陣列，每一項目包含：

* 權限套用的範圍，擇一
    - `scope`: 特定身分。接受公開 (`*`)、工作人員 (`staff`)、系統管理者 (`admin`)
    - `user`: 特定的使用者名稱
    - `group`: 特定的群組名稱
* `type`: 權限種類，接受 `view`, `comment`, `edit`。
* `effect`: 權限效果，可以是允許 (`allow`) 或是拒絕 (`deny`)。

#### DELETE

將文件或資料夾移至垃圾桶。

議題追蹤系統 (issue tracker)
---
### /issues/

#### GET

傳回議題列表。接受以下篩選參數：

* `state`: 議題狀態，接受待處理 (`open`)、已結案 (`closed`)、全部 (`all`)，預設為 `open`。
* `labels`: 標有特定標籤。
* `created`: 由特定使用者建立。
* `assigned`: 指派給特定使用者。
* `starred`: 目前的使用者已標記星號。

### /issues/new

#### POST

建立新議題。

### /issues/`id`

#### GET

取得議題資訊。

#### POST

對議題進行操作，接受以下任一參數：

* `star`/`unstar`
* `comment`
* `assign`
* `close`/`reopen`
* `label`

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

### GET

#### (`nid`)
取得文件或資料夾節點資訊，物件皆以節點ID (nid) 識別。  
當物件不存在，傳回 **HTTP 400** `{"status": "invalid_property"}`。  
當不具物件的檢視權限，傳回 **HTTP 403** `{"status": "permission_denied"}`。  

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


議題追蹤系統 (issue tracker)
---
（建構中）

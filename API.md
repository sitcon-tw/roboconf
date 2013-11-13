staff.sitcon.org API
===

工作人員資訊
---
端點：/users/api

### GET
列出工作人員。範例：
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

### GET(`name`)
取得個別工作人員資訊。範例：
```
{
    "status": "success",
    "name": "RSChiang",
    "title": "行政組長",
    "avatar": "https://secure.gravatar.com/..."
}
```
當使用者不存在或無效，傳回 **HTTP 400** `{"status": "invalid"}`

議題追蹤系統 (issue tracker)
---
（建構中）

文件系統
---
端點：/docs/api

文件系統的物件皆以節點ID (nid) 識別。

### GET(`nid`)
取得文件或資料夾節點資訊。範例：
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
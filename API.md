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
當使用者不存在或無效，傳回 `{"status": "invalid"}`

議題追蹤系統 (issue tracker)
---
（建構中）

文件系統
---
（建構中）

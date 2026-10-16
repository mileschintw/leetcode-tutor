---
type: regex
target: mock_calls
pattern: '\A(?:(?!"tool":\s*"(?:[\w-]+__)?notion-create-pages")[\s\S])*"tool":\s*"(?:[\w-]+__)?notion-(?:update-data-source"|create-database"(?:(?!"verdict":).)*?MULTI_SELECT\(\\*'')'
---

Before it creates any page, the push gives the data source the plan's Tags and Lists options, either in the new database's schema or with notion-update-data-source, because Notion rejects a multi-select value that isn't an existing option.

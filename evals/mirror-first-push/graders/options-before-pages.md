---
type: regex
target: mock_calls
pattern: '\A(?:(?!"tool":\s*"(?:[\w-]+__)?notion-create-pages")[\s\S])*"tool":\s*"(?:[\w-]+__)?notion-update-data-source"'
---

Before it creates any page, the push adds the plan's Tags and Lists values to the data source's options with notion-update-data-source, because Notion rejects a multi-select value that isn't an existing option.

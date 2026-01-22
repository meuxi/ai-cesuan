# RAG 知识库数据目录

此目录用于存放知识库源数据文件。

## 支持的文件格式

- **JSON** (.json) - 结构化数据，推荐格式
- **Markdown** (.md) - 文档、教程
- **Text** (.txt) - 纯文本

## 目录结构建议

```
data/
├── bazi/           # 八字相关知识
├── liuyao/         # 六爻相关知识
├── tarot/          # 塔罗牌知识
├── qimen/          # 奇门遁甲知识
├── ziwei/          # 紫微斗数知识
├── meihua/         # 梅花易数知识
├── xiaoliu/        # 小六壬知识
├── wuxing/         # 五行知识
├── terminology/    # 术语解释
└── general/        # 通用知识
```

## JSON 数据格式示例

```json
{
  "documents": [
    {
      "title": "文档标题",
      "content": "文档内容...",
      "category": "bazi",
      "metadata": {
        "source": "来源",
        "author": "作者"
      }
    }
  ]
}
```

## 使用方法

### 1. 通过 API 加载目录

```bash
POST /api/rag/knowledge-bases/{kb_id}/documents/from-directory
{
  "directory": "/path/to/data",
  "recursive": true
}
```

### 2. 通过 Python 代码加载

```python
from src.rag import get_rag_service

service = get_rag_service()
kb = service.create_knowledge_base("八字知识库", category="bazi")
await service.add_documents_from_directory(kb.id, "./data/bazi")
```

## 注意事项

1. 文件编码必须为 UTF-8
2. JSON 文件需符合标准格式
3. 大文件会自动分块处理
4. 建议按主题组织目录结构

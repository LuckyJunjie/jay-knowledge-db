# Jay Knowledge DB - FAQ

## 概述
Jay Knowledge DB 是一个 NLP 知识库，包含向量嵌入、情感分析和文本分类功能。

## 快速开始

```python
from nlp import Embeddings, SentimentAnalyzer, TextClassifier, Pipeline

# 1. 向量嵌入
emb = Embeddings()
vec = emb.encode("Hello world")

# 2. 情感分析
sa = SentimentAnalyzer()
result = sa.analyze("I love this!")

# 3. 文本分类
tc = TextClassifier()
label = tc.classify("AI is amazing")

# 4. 流水线
pipe = Pipeline()
output = pipe.process("Your text here")
```

## API 参考

### Embeddings
- `encode(text)` - 将文本转换为向量
- `batch_encode(texts)` - 批量转换

### SentimentAnalyzer
- `analyze(text)` - 返回 'positive'/'negative'/'neutral'
- `get_score()` - 返回置信度分数

### TextClassifier
- `classify(text)` - 返回分类标签
- `get_top_k(k)` - 返回 Top-K 分类结果

### Pipeline
- `process(text)` - 完整处理流程
- `set_components()` - 自定义组件
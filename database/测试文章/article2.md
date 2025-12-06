# Python FastAPI 快速入门

## 简介

FastAPI 是一个现代、快速（高性能）的 Web 框架，用于构建 API，基于 Python 3.7+ 的标准类型提示。它具有以下特点：

- **快速**: 性能与 NodeJS 和 Go 相当
- **快速编码**: 开发速度提高约 200% 到 300%
- **更少的 Bug**: 减少约 40% 的人为错误
- **直观**: 强大的编辑器支持，自动补全
- **简单**: 易于学习和使用
- **标准化**: 基于 OpenAPI 和 JSON Schema

## 安装

```bash
pip install fastapi
pip install uvicorn[standard]
```

## 第一个 API

创建一个 `main.py` 文件：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

运行服务器：

```bash
uvicorn main:app --reload
```

## 请求体与数据验证

FastAPI 使用 Pydantic 进行数据验证：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

## 自动文档

FastAPI 自动生成交互式 API 文档：

- **Swagger UI**: 访问 `/docs`
- **ReDoc**: 访问 `/redoc`

## 数据库集成

FastAPI 可以与任何数据库配合使用，常见的选择是 SQLAlchemy：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

## 总结

FastAPI 是构建现代 API 的绝佳选择，它结合了 Python 的简洁性和高性能，同时提供了出色的开发体验。无论是小型项目还是大型应用，FastAPI 都能胜任。

---

*推荐阅读: FastAPI 官方文档 https://fastapi.tiangolo.com/*

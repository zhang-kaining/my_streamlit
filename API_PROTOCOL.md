# 前后端交互协议文档

## 接口概述

本文档定义了 AI Chat Assistant 前端（Streamlit）与后端（Gemini Service）之间的 HTTP API 交互协议。

## 接口信息

- **端点**: `/invocations`
- **方法**: `POST`
- **Content-Type**: `application/json`
- **超时时间**: 30 秒

## 请求格式 (Request)

### 请求示例

```json
{
  "model": "gemini-2.5-flash-lite",
  "messages": [
    {
      "role": "user",
      "content": "你好"
    },
    {
      "role": "assistant",
      "content": "你好！有什么我可以帮助你的吗？"
    },
    {
      "role": "user",
      "content": "介绍一下 Python"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称，默认 "gemini-2.5-flash-lite" |
| `messages` | array | 是 | 对话历史数组，按时间顺序排列 |
| `messages[].role` | string | 是 | 角色类型，可选值: "user" 或 "assistant" |
| `messages[].content` | string | 是 | 消息内容文本 |

### 注意事项

- `messages` 数组包含完整的对话历史，用于保持上下文连贯性
- 消息按时间顺序排列，最新的消息在数组末尾
- 每次请求都会发送完整的对话历史

## 响应格式 (Response)

### 成功响应 (HTTP 200)

```json
{
  "response": "Python 是一种高级编程语言...",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 80,
    "total_tokens": 230
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `response` | string | 是 | AI 生成的回复文本 |
| `usage` | object | 否 | Token 使用统计信息 |
| `usage.prompt_tokens` | integer | 否 | 输入消息消耗的 token 数量 |
| `usage.completion_tokens` | integer | 否 | 生成回复消耗的 token 数量 |
| `usage.total_tokens` | integer | 否 | 总 token 数量（prompt + completion） |

### 错误响应 (HTTP 非 200)

当后端返回非 200 状态码时，前端会显示错误信息：

```
❌ Error: API returned status code {status_code}
```

## 角色映射规则

前后端使用不同的角色命名约定：

| 前端角色 | 后端角色 (Gemini) | 说明 |
|---------|------------------|------|
| `user` | `user` | 用户消息 |
| `assistant` | `model` | AI 助手消息 |

后端会自动进行角色转换：
```python
role = "model" if msg["role"] == "assistant" else msg["role"]
```

## 错误处理

### 连接超时
- **触发条件**: 请求超过 30 秒未响应
- **前端处理**: 显示超时错误信息

### 连接失败
- **触发条件**: 无法连接到后端服务
- **前端处理**: 显示连接失败错误信息
- **可能原因**: 
  - 后端服务未启动
  - API URL 配置错误
  - 网络问题

### 异常捕获
- 所有未预期的异常都会被捕获
- 前端显示: `❌ Unknown error: {error_message}`

## 支持的 API 地址

前端支持以下 API 地址选项（可在侧边栏切换）：

1. `http://localhost:8080/invocations` (默认)
2. `http://localhost:5000/api/chat`
3. `http://127.0.0.1:8080/invocations`

## 完整调用示例

### cURL 示例

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-lite",
    "messages": [
      {
        "role": "user",
        "content": "你好"
      }
    ]
  }'
```

### Python 示例

```python
import requests

url = "http://localhost:8080/invocations"
payload = {
    "model": "gemini-2.5-flash-lite",
    "messages": [
        {"role": "user", "content": "你好"}
    ]
}

response = requests.post(url, json=payload, timeout=30)

if response.status_code == 200:
    data = response.json()
    print(f"回复: {data['response']}")
    print(f"Token 使用: {data['usage']}")
else:
    print(f"错误: {response.status_code}")
```

## 版本信息

- **协议版本**: 1.0
- **最后更新**: 2025-11-17
- **模型**: gemini-2.5-flash-lite

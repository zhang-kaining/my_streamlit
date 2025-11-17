# AI 对话助手 - Streamlit 应用

一个简洁、规范的 Streamlit 对话界面，用于与后端模型服务交互。

## 项目结构

```
.
├── app.py                         # 前端应用文件
├── config.py                      # 配置文件
├── requirements.txt               # 依赖管理
├── llm/                           # 后端服务目录
│   ├── base.py                    # LLM 基类
│   └── gemini_service.py          # Gemini 服务实现
├── .gitignore                     # Git 忽略文件
└── README.md                      # 项目文档
```

## 快速开始

### 1. 配置 API Key

后端服务需要 Gemini API Key 才能运行。

#### 获取 API Key
访问 [Google AI Studio](https://aistudio.google.com/apikey) 申请免费的 Gemini API Key。

#### 配置环境变量
在项目根目录创建 `.env` 文件：

```bash
GEMINI_API_KEY=your_api_key_here
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动后端服务

```bash
cd llm
python gemini_service.py
```

后端服务会在 `http://localhost:8080` 启动。

### 4. 启动前端应用

在另一个终端窗口运行：

```bash
streamlit run app.py
```

应用会自动在浏览器打开：http://localhost:8501

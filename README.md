# MCP Reddit Translator - Reddit 服务器（基础版 + 翻译增强版）

## 简介

MCP Reddit Translator 是一个基于 Model Context Protocol (MCP) 的 Reddit 服务器，提供两种使用模式：

1. **基础版本**：标准的 Reddit 内容获取功能
2. **翻译增强版**：在基础功能上增加**自动英文到中文翻译**功能

无论选择哪种模式，都可以让 AI 助手快速获取 Reddit 的热门帖子和讨论内容。翻译增强版特别适合中文用户，让阅读和理解英文 Reddit 内容更加轻松。

## 主要功能

### 🔧 基础功能（两种模式都支持）
- 🔥 获取任意 subreddit 的热门话题和讨论内容
- 📝 抓取帖子详细信息，包括评论和互动数据
- 🔍 搜索 Reddit 中的相关内容和帖子
- 🖼️ 支持文本、链接、图集等多种 Reddit 内容类型
- 🛠️ 提供命令行工具，方便开发者测试和调试
- 🔌 与 Claude Desktop 等 MCP 客户端无缝集成

### 🌐 翻译增强功能（仅翻译增强版）
- 🌐 **自动英文到中文翻译**（支持多种翻译服务）
- 🧠 **智能语言检测**，仅翻译英文内容
- 💾 **翻译缓存**，提高响应速度
- 🎛️ **可选翻译**，每个工具都支持启用/禁用翻译功能
- 🔧 **多服务支持**：Google Translate、DeepL、百度翻译、腾讯翻译、OpenAI GPT

## 快速开始

### 1. 安装 uv（推荐）

本项目使用 `uv` 来管理依赖和运行环境，请先安装 uv：

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip 安装
pip install uv
```

### 2. 配置 MCP 客户端

根据你的需求选择以下配置之一：

#### 选项 A：基础版本配置（仅 Reddit 功能）

如果你只需要基础的 Reddit 内容获取功能，使用以下配置：

```json
{
  "mcpServers": {
    "mcp-reddit-basic": {
      "command": "uv",
      "args": [
        "--quiet",
        "run",
        "--with", "requests",
        "--with", "mcp>=1.0.0", 
        "--python", "3.11",
        "--",
        "python",
        "-c",
        "import requests; exec(requests.get('https://raw.githubusercontent.com/Metres0/mcp-reddit-translator/main/reddit_translator.py').text)"
      ],
      "env": {
        "ENABLE_TRANSLATION": "false"
      }
    }
  }
}
```

#### 选项 B：翻译增强版配置（Reddit + 自动翻译）

如需启用自动翻译功能，使用以下配置：

```json
{
  "mcpServers": {
    "mcp-reddit-translator": {
      "command": "uv",
      "args": [
        "--quiet",
        "run",
        "--with", "requests",
        "--with", "mcp>=1.0.0",
        "--with", "translate",
        "--with", "openai",
        "--with", "anthropic",
        "--python", "3.11",
        "--",
        "python",
        "-c",
        "import requests; exec(requests.get('https://raw.githubusercontent.com/Metres0/mcp-reddit-translator/main/reddit_translator.py').text)"
      ],
      "env": {
        "TRANSLATION_SERVICE": "google",
        "ENABLE_TRANSLATION": "true",
        "ENABLE_CACHE": "true"
      }
    }
  }
}
```

### 3. 配置翻译服务（可选）

编辑 `translation_config.json` 文件来配置翻译服务：

```json
{
  "translation": {
    "enabled": true,
    "target_language": "zh",
    "service": "google",
    "services": {
      "google": {
        "enabled": true,
        "api_key": "your-google-api-key",
        "endpoint": "https://translation.googleapis.com/language/translate/v2"
      }
    }
  }
}
```

详细配置说明请参考 [TRANSLATION_SETUP.md](TRANSLATION_SETUP.md)。

### 备用方法：本地安装

如果你不想使用 `uv`，也可以下载脚本到本地运行：

```bash
# 下载脚本
wget https://raw.githubusercontent.com/Metres0/mcp-reddit-translator/main/reddit_translator.py

# 安装依赖
pip install -r https://raw.githubusercontent.com/Metres0/mcp-reddit-translator/main/requirements.txt
```

然后在 MCP 配置中使用本地路径：

```json
{
  "mcpServers": {
    "mcp-reddit-translator": {
      "command": "python3",
      "args": ["./reddit_translator.py"],
      "env": {
        "TRANSLATION_SERVICE": "google",
        "ENABLE_TRANSLATION": "true",
        "ENABLE_CACHE": "true"
      }
    }
  }
}
```

## 支持的工具

### 1. fetch_hot_threads
获取指定 subreddit 的热门帖子

**参数：**
- `subreddit` (必需): subreddit 名称（不包含 r/ 前缀）
- `limit` (可选): 返回帖子数量，默认 10，范围 1-50
- `translate` (可选): 是否启用自动翻译，默认 true

### 2. fetch_post_details
获取指定帖子的详细信息和评论

**参数：**
- `post_id` (必需): Reddit 帖子 ID
- `translate` (可选): 是否启用自动翻译，默认 true

### 3. search_posts
在 Reddit 中搜索帖子

**参数：**
- `query` (必需): 搜索关键词
- `subreddit` (可选): 限制搜索的 subreddit
- `translate` (可选): 是否启用自动翻译，默认 true

## 使用示例

### 基础版本使用示例

#### 1. 获取热门帖子（基础版本）

```json
{
  "method": "tools/call",
  "params": {
    "name": "fetch_hot_threads",
    "arguments": {
      "subreddit": "python",
      "limit": 5
    }
  }
}
```

**输出示例（基础版本）：**
```
📍 r/python 热门帖子 (共 5 个):

1. 🔥 What's the best Python framework for beginners?
   👤 作者: user123 | 👍 1.2k | 💬 234 | 🕒 2024-01-15

2. 🔥 Python 3.12 Performance Improvements
   👤 作者: dev_user | 👍 856 | 💬 127 | 🕒 2024-01-14
```

### 翻译增强版使用示例

#### 1. 获取热门帖子（禁用翻译）

```json
{
  "method": "tools/call",
  "params": {
    "name": "fetch_hot_threads",
    "arguments": {
      "subreddit": "python",
      "limit": 5,
      "translate": false
    }
  }
}
```

**输出示例（禁用翻译）：**
```
📍 r/python 热门帖子 (共 5 个):

1. 🔥 What's the best Python framework for beginners?
   👤 作者: user123 | 👍 1.2k | 💬 234 | 🕒 2024-01-15

2. 🔥 Python 3.12 Performance Improvements
   👤 作者: dev_user | 👍 856 | 💬 127 | 🕒 2024-01-14
```

#### 2. 获取热门帖子（启用翻译）

```json
{
  "method": "tools/call",
  "params": {
    "name": "fetch_hot_threads",
    "arguments": {
      "subreddit": "python",
      "limit": 5,
      "translate": true
    }
  }
}
```

**输出示例（启用翻译）：**
```
📍 r/python 热门帖子 (共 5 个):

1. 🔥 What's the best Python framework for beginners?
   中文: 对于初学者来说，最好的 Python 框架是什么？
   👤 作者: user123 | 👍 1.2k | 💬 234 | 🕒 2024-01-15

2. 🔥 Python 3.12 Performance Improvements
   中文: Python 3.12 性能改进
   👤 作者: dev_user | 👍 856 | 💬 127 | 🕒 2024-01-14
```

#### 3. 获取特定帖子详情（翻译增强版）

```json
{
  "method": "tools/call",
  "params": {
    "name": "fetch_post_details",
    "arguments": {
      "post_id": "abc123",
      "translate": true
    }
  }
}
```

#### 4. 搜索帖子（翻译增强版）

```json
{
  "method": "tools/call",
  "params": {
    "name": "search_posts",
    "arguments": {
      "query": "machine learning",
      "subreddit": "MachineLearning",
      "translate": true
    }
  }
}
```

> **注意**：基础版本中，所有工具都不包含 `translate` 参数，因为翻译功能被禁用。翻译增强版中，每个工具都支持可选的 `translate` 参数来控制是否启用翻译。

## 支持的内容类型

### 文本帖子
- 完整的帖子内容
- 格式化的 Markdown 文本
- 代码块和引用

### 链接帖子
- 外部链接 URL
- 链接预览信息
- 域名和来源识别

### 图片和媒体
- 图片 URL 和描述
- 视频链接
- GIF 动图
- 图集和相册

### 评论数据
- 评论内容和层级结构
- 点赞数和回复数
- 评论时间和作者信息

## 常用 Subreddit 推荐

### 技术类
- r/programming - 编程讨论
- r/MachineLearning - 机器学习
- r/webdev - Web 开发
- r/Python - Python 编程
- r/javascript - JavaScript

### 新闻资讯
- r/technology - 科技新闻
- r/worldnews - 国际新闻
- r/science - 科学研究

### 生活娱乐
- r/AskReddit - 问答讨论
- r/todayilearned - 今日学到
- r/explainlikeimfive - 简单解释

## 注意事项

1. **API 限制**: Reddit API 有访问频率限制，请合理使用
2. **内容过滤**: 某些敏感内容可能无法获取
3. **实时性**: 数据可能有几分钟的延迟
4. **隐私保护**: 不会获取用户个人信息

## 故障排除

### 常见问题

**Q: 无法获取某个 subreddit 的内容？**
A: 检查 subreddit 名称是否正确，某些私有或受限制的社区无法访问。

**Q: 获取的内容不完整？**
A: 可能是由于 API 限制或网络问题，稍后重试。

**Q: 图片无法显示？**
A: 某些图片可能需要 Reddit 登录才能查看，或者链接已失效。

## 支持的翻译服务

- 🌐 **Google Translate** - 免费额度，高质量翻译
- 🔷 **DeepL** - 专业翻译，支持更自然的表达
- 🔵 **百度翻译** - 中文优化，本土化支持
- 🟢 **腾讯翻译君** - 快速响应，稳定可靠
- 🤖 **OpenAI GPT** - AI 驱动，上下文理解

## 项目文件说明

- `reddit_translator.py` - 主要的 MCP 服务器文件
- `translation_config.json` - 翻译服务配置文件
- `mcp_config.json` - MCP 客户端配置示例
- `requirements.txt` - Python 依赖列表
- `TRANSLATION_SETUP.md` - 详细的翻译配置指南
- `INSTALLATION.md` - 安装和部署指南

## 测试和验证

运行测试脚本验证功能：

```bash
# 基础功能测试
python3 test_reddit_mcp.py

# 翻译功能测试
python3 test_translation.py

# 演示脚本
python3 demo.py
```

## 更多资源

- [GitHub 项目地址](https://github.com/Metres0/mcp-reddit-translator)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Reddit API 文档](https://www.reddit.com/dev/api/)
- [翻译配置指南](TRANSLATION_SETUP.md)
- [安装部署指南](INSTALLATION.md)

---

通过 MCP Reddit Translator，你可以轻松地让 AI 助手帮你浏览和分析 Reddit 上的热门内容，**自动翻译成中文**，获取最新的技术动态、新闻资讯和社区讨论，无需担心语言障碍。
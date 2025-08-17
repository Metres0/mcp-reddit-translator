# MCP Reddit Translator - 增强版 Reddit 服务器

## 简介

MCP Reddit Translator 是一个基于 Model Context Protocol (MCP) 的增强版 Reddit 服务器，不仅可以让 AI 助手快速获取 Reddit 的热门帖子和讨论内容，还支持**自动英文到中文翻译**功能，让中文用户更轻松地阅读和理解 Reddit 内容。

## 主要功能

- 🔥 获取任意 subreddit 的热门话题和讨论内容
- 📝 抓取帖子详细信息，包括评论和互动数据
- 🔍 搜索 Reddit 中的相关内容和帖子
- 🖼️ 支持文本、链接、图集等多种 Reddit 内容类型
- 🌐 **自动英文到中文翻译**（支持多种翻译服务）
- 🧠 **智能语言检测**，仅翻译英文内容
- 💾 **翻译缓存**，提高响应速度
- 🎛️ **可选翻译**，每个工具都支持启用/禁用翻译功能
- 🛠️ 提供命令行工具，方便开发者测试和调试
- 🔌 与 Claude Desktop 等 MCP 客户端无缝集成

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 MCP 客户端

#### 基础配置（仅 Reddit 功能）

将以下配置添加到你的 MCP 客户端配置文件中（如 Claude Desktop 的 `claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "mcp-reddit-translator": {
      "command": "python3",
      "args": ["./reddit_translator.py"]
    }
  }
}
```

#### 增强配置（带翻译功能）

如需启用自动翻译功能，使用以下配置：

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

### 1. 获取热门帖子（基础功能）

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

**输出示例（无翻译）：**
```
📍 r/python 热门帖子 (共 5 个):

1. 🔥 What's the best Python framework for beginners?
   👤 作者: user123 | 👍 1.2k | 💬 234 | 🕒 2024-01-15

2. 🔥 Python 3.12 Performance Improvements
   👤 作者: dev_user | 👍 856 | 💬 127 | 🕒 2024-01-14
```

### 2. 获取热门帖子（带自动翻译）

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

**输出示例（带翻译）：**
```
📍 r/python 热门帖子 (共 5 个):

1. 🔥 What's the best Python framework for beginners?
   中文: 对于初学者来说，最好的 Python 框架是什么？
   👤 作者: user123 | 👍 1.2k | 💬 234 | 🕒 2024-01-15

2. 🔥 Python 3.12 Performance Improvements
   中文: Python 3.12 性能改进
   👤 作者: dev_user | 👍 856 | 💬 127 | 🕒 2024-01-14
```

### 3. 获取特定帖子详情

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

### 4. 搜索帖子

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

### 3. 搜索特定主题

```
用户: 搜索一下关于 AI 和机器学习的最新讨论

AI: 我来搜索相关的讨论...

[调用 search_posts 工具]
参数: query: "AI machine learning", subreddit: "MachineLearning"

找到以下相关讨论:
1. "GPT-4 在代码生成方面的新突破"
2. "机器学习模型部署的最佳实践"
3. "开源 AI 工具推荐清单"
...
```

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
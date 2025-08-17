# MCP Reddit Translator - 增强版 Reddit 服务器

## 简介

MCP Reddit Translator 是一个基于 Model Context Protocol (MCP) 的增强版 Reddit 服务器，不仅可以让 AI 助手快速获取 Reddit 的热门帖子和讨论内容，还支持**自动英文到中文翻译**功能，让中文用户更轻松地阅读和理解 Reddit 内容。

## 主要功能

- 🔥 获取任意 subreddit 的热门话题和讨论内容
- 📝 抓取帖子详细信息，包括评论和互动数据
- 🖼️ 支持文本、链接、图集等多种 Reddit 内容类型
- 🌐 **自动英文到中文翻译**（支持多种翻译服务）
- 🧠 **智能语言检测**，仅翻译英文内容
- 💾 **翻译缓存**，提高响应速度
- 🛠️ 提供命令行工具，方便开发者测试和调试
- 🔌 与 Claude Desktop 等 MCP 客户端无缝集成

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 MCP 客户端

将以下配置添加到你的 MCP 客户端配置文件中（如 Claude Desktop 的 `claude_desktop_config.json`）：

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

## 使用示例

### 1. 获取热门帖子（带自动翻译）

```
用户: 帮我看看 r/programming 最新的热门帖子

AI: 我来为你获取 r/programming 的热门帖子...

[调用 fetch_hot_threads 工具]
参数: subreddit: programming

结果显示当前热门话题包括:
1. "New JavaScript Framework Released" 
   翻译: "新的 JavaScript 框架发布" - 1.2k 点赞
2. "Python 3.12 Performance Optimization Guide"
   翻译: "Python 3.12 性能优化详解" - 890 点赞
3. "Best Practices for Open Source Project Maintenance"
   翻译: "开源项目维护的最佳实践" - 756 点赞
...
```

### 2. 获取特定帖子详情

```
用户: 能详细看看第一个帖子的内容和评论吗？

AI: 我来获取这个帖子的详细信息...

[调用 fetch_post_details 工具]
参数: post_id: xyz123

帖子详情:
标题: 新的 JavaScript 框架发布
作者: developer_user
发布时间: 2小时前
内容: [完整帖子内容]

热门评论:
1. "这个框架解决了我们项目的痛点" - 45 点赞
2. "文档写得很详细，值得尝试" - 32 点赞
...
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
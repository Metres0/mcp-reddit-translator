# MCP Reddit Server 安装配置指南

## 系统要求

- Python 3.8 或更高版本
- uv 包管理器
- Claude Desktop 或其他支持 MCP 的客户端

## 快速开始

### 1. 安装 uv 包管理器

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**使用 pip:**
```bash
pip install uv
```

### 2. 验证安装

```bash
uv --version
```

### 3. 测试 MCP Reddit Server

```bash
# 直接运行测试
uvx --from git+https://github.com/adhikasp/mcp-reddit.git mcp-reddit --help
```

## Claude Desktop 集成

### 1. 找到配置文件位置

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/claude/claude_desktop_config.json
```

### 2. 编辑配置文件

如果配置文件不存在，创建一个新的。将以下内容添加到配置文件中：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
      "env": {}
    }
  }
}
```

如果已有其他 MCP 服务器配置，只需在 `mcpServers` 对象中添加 `reddit` 配置：

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "existing-command",
      "args": ["existing-args"]
    },
    "reddit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
      "env": {}
    }
  }
}
```

### 3. 重启 Claude Desktop

保存配置文件后，完全退出并重新启动 Claude Desktop。

### 4. 验证集成

在 Claude Desktop 中输入以下测试命令：

```
帮我获取 r/programming 的热门帖子
```

如果配置正确，Claude 应该能够调用 Reddit MCP 服务器并返回热门帖子信息。

## 其他 MCP 客户端集成

### Continue.dev

在 Continue 的配置文件中添加：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"]
    }
  }
}
```

### 自定义 MCP 客户端

如果你在开发自己的 MCP 客户端，可以使用以下方式启动 Reddit 服务器：

```python
import subprocess

# 启动 MCP Reddit Server
process = subprocess.Popen([
    "uvx", 
    "--from", "git+https://github.com/adhikasp/mcp-reddit.git", 
    "mcp-reddit"
], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 通过 stdin/stdout 与服务器通信
# 发送 MCP 协议消息...
```

## 高级配置

### 环境变量配置

你可以通过环境变量来配置 Reddit API 的行为：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
      "env": {
        "REDDIT_USER_AGENT": "MyApp/1.0",
        "REDDIT_TIMEOUT": "30"
      }
    }
  }
}
```

### 本地开发模式

如果你想修改或调试 MCP Reddit Server，可以克隆仓库到本地：

```bash
# 克隆仓库
git clone https://github.com/adhikasp/mcp-reddit.git
cd mcp-reddit

# 安装依赖
uv sync

# 本地运行
uv run mcp-reddit
```

然后在配置文件中使用本地路径：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-reddit", "mcp-reddit"],
      "env": {}
    }
  }
}
```

## 故障排除

### 常见问题

**1. "uvx 命令未找到"**

确保已正确安装 uv：
```bash
# 重新安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 重新加载 shell 配置
source ~/.bashrc  # 或 ~/.zshrc
```

**2. "无法连接到 Reddit"**

检查网络连接和防火墙设置：
```bash
# 测试网络连接
curl -I https://www.reddit.com

# 检查 DNS 解析
nslookup reddit.com
```

**3. "MCP 服务器启动失败"**

检查配置文件格式：
```bash
# 验证 JSON 格式
python -m json.tool claude_desktop_config.json
```

**4. "权限被拒绝"**

某些 subreddit 可能是私有的或需要特殊权限：
```
# 尝试访问公开的 subreddit
r/programming
r/Python
r/technology
```

### 调试模式

启用详细日志输出：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
      "env": {
        "DEBUG": "1",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### 性能优化

**缓存配置:**
```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
      "env": {
        "CACHE_TTL": "300",
        "MAX_CACHE_SIZE": "100"
      }
    }
  }
}
```

**请求限制:**
```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
      "env": {
        "RATE_LIMIT": "60",
        "BURST_LIMIT": "10"
      }
    }
  }
}
```

## 安全注意事项

1. **API 密钥管理**: 如果使用 Reddit API 密钥，不要将其硬编码在配置文件中
2. **网络安全**: 确保网络连接安全，避免在不安全的网络环境中使用
3. **内容过滤**: 注意 Reddit 内容可能包含不当信息，建议启用内容过滤
4. **隐私保护**: 服务器不会存储个人信息，但请注意数据传输的隐私性

## 更新和维护

### 更新 MCP Reddit Server

```bash
# uv 会自动获取最新版本
uvx --from git+https://github.com/adhikasp/mcp-reddit.git mcp-reddit --version
```

### 清理缓存

```bash
# 清理 uv 缓存
uv cache clean

# 清理特定包缓存
uv cache clean mcp-reddit
```

## 获取帮助

- [GitHub Issues](https://github.com/adhikasp/mcp-reddit/issues)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Reddit API 文档](https://www.reddit.com/dev/api/)

---

按照以上步骤，你应该能够成功安装和配置 MCP Reddit Server。如果遇到问题，请参考故障排除部分或在 GitHub 上提交 Issue。
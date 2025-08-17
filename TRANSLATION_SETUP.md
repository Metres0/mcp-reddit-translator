# 翻译功能配置指南

本指南将帮助您配置 MCP Reddit Server 的自动翻译功能，支持多种翻译服务。

## 🌐 支持的翻译服务

### 1. Google 翻译（推荐新手）
- **优点**: 免费，无需注册，即开即用
- **缺点**: 翻译质量中等，有使用频率限制
- **配置**: 无需配置

### 2. DeepL 翻译（推荐高质量）
- **优点**: 翻译质量最高，特别适合技术文档
- **缺点**: 需要注册，有免费额度限制
- **免费额度**: 500,000字符/月
- **配置**: 需要API密钥

### 3. 百度翻译（推荐国内用户）
- **优点**: 国内服务稳定，免费额度大
- **缺点**: 需要实名认证
- **免费额度**: 200万字符/月
- **配置**: 需要APP ID和密钥

### 4. 腾讯翻译（企业推荐）
- **优点**: 企业级服务，稳定性好
- **缺点**: 配置相对复杂
- **免费额度**: 500万字符/月
- **配置**: 需要SecretId和SecretKey

### 5. OpenAI GPT 翻译（最高质量）
- **优点**: 翻译质量最高，理解上下文
- **缺点**: 成本较高，速度较慢
- **配置**: 需要OpenAI API密钥

## 🚀 快速开始

### 方式一：使用免费Google翻译（零配置）

```bash
# 直接运行，使用默认Google翻译
python reddit_translator.py
```

### 方式二：配置高质量翻译服务

1. 编辑 `translation_config.json` 文件
2. 选择翻译服务并填入API密钥
3. 运行脚本

## 📝 详细配置步骤

### DeepL 翻译配置

1. **注册DeepL账户**
   - 访问 [DeepL API](https://www.deepl.com/pro-api)
   - 注册免费账户
   - 获取API密钥

2. **配置文件设置**
   ```json
   {
     "service": "deepl",
     "api_key": "your-deepl-api-key-here",
     "enabled": true
   }
   ```

3. **环境变量设置（可选）**
   ```bash
   export TRANSLATION_SERVICE=deepl
   export TRANSLATION_API_KEY=your-deepl-api-key
   ```

### 百度翻译配置

1. **注册百度开发者账户**
   - 访问 [百度翻译开放平台](https://fanyi-api.baidu.com/)
   - 注册并实名认证
   - 创建应用获取APP ID和密钥

2. **配置文件设置**
   ```json
   {
     "service": "baidu",
     "api_key": "your-baidu-app-id",
     "secret_key": "your-baidu-secret-key",
     "enabled": true
   }
   ```

3. **环境变量设置（可选）**
   ```bash
   export TRANSLATION_SERVICE=baidu
   export TRANSLATION_API_KEY=your-baidu-app-id
   export TRANSLATION_SECRET_KEY=your-baidu-secret-key
   ```

### OpenAI GPT 翻译配置

1. **获取OpenAI API密钥**
   - 访问 [OpenAI API](https://platform.openai.com/api-keys)
   - 创建API密钥
   - 确保账户有足够余额

2. **配置文件设置**
   ```json
   {
     "service": "openai",
     "api_key": "your-openai-api-key",
     "model": "gpt-3.5-turbo",
     "enabled": true
   }
   ```

3. **环境变量设置（可选）**
   ```bash
   export TRANSLATION_SERVICE=openai
   export TRANSLATION_API_KEY=your-openai-api-key
   export TRANSLATION_MODEL=gpt-3.5-turbo
   ```

## ⚙️ 高级配置选项

### 翻译缓存
```json
{
  "cache_enabled": true,
  "max_length": 5000,
  "batch_size": 10
}
```

### 翻译质量控制
```json
{
  "min_confidence": 0.8,
  "fallback_service": "google",
  "retry_attempts": 3
}
```

### 内容过滤
```json
{
  "skip_short_text": true,
  "min_text_length": 10,
  "skip_code_blocks": true,
  "skip_urls": true
}
```

## 🔧 安装依赖

```bash
# 安装Python依赖
pip install aiohttp asyncio

# 或使用requirements.txt
pip install -r requirements.txt
```

创建 `requirements.txt` 文件：
```
aiohttp>=3.8.0
asyncio-throttle>=1.0.0
requests>=2.28.0
```

## 🧪 测试配置

### 测试翻译功能
```bash
# 测试基本翻译
python -c "import asyncio; from reddit_translator import *; asyncio.run(TranslationManager(load_translation_config()).translate_text('Hello World'))"

# 运行完整演示
python reddit_translator.py
```

### 验证API连接
```bash
# 创建测试脚本
cat > test_translation.py << 'EOF'
import asyncio
from reddit_translator import load_translation_config, TranslationManager

async def test_translation():
    config = load_translation_config()
    manager = TranslationManager(config)
    
    test_text = "Hello, this is a test message for translation."
    result = await manager.translate_text(test_text)
    
    print(f"原文: {test_text}")
    print(f"译文: {result}")
    print(f"服务: {config.service}")

if __name__ == "__main__":
    asyncio.run(test_translation())
EOF

# 运行测试
python test_translation.py
```

## 🚨 故障排除

### 常见问题

1. **翻译服务无响应**
   ```bash
   # 检查网络连接
   ping google.com
   
   # 检查API密钥
   echo $TRANSLATION_API_KEY
   ```

2. **API配额超限**
   - 检查API使用量
   - 切换到其他翻译服务
   - 启用翻译缓存减少API调用

3. **翻译质量不佳**
   - 尝试DeepL或OpenAI服务
   - 调整文本预处理设置
   - 检查源文本是否包含特殊字符

### 调试模式
```bash
# 启用详细日志
export TRANSLATION_DEBUG=true
python reddit_translator.py
```

### 性能优化
```json
{
  "cache_enabled": true,
  "batch_size": 20,
  "concurrent_requests": 5,
  "request_timeout": 30
}
```

## 📊 使用统计

### 监控翻译使用量
```bash
# 创建使用统计脚本
cat > translation_stats.py << 'EOF'
import json
from datetime import datetime

def log_translation_usage(service, characters, cost=0):
    stats_file = "translation_stats.json"
    
    try:
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    except FileNotFoundError:
        stats = {"daily_usage": {}, "total_usage": {}}
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in stats["daily_usage"]:
        stats["daily_usage"][today] = {}
    
    if service not in stats["daily_usage"][today]:
        stats["daily_usage"][today][service] = {"characters": 0, "cost": 0}
    
    stats["daily_usage"][today][service]["characters"] += characters
    stats["daily_usage"][today][service]["cost"] += cost
    
    if service not in stats["total_usage"]:
        stats["total_usage"][service] = {"characters": 0, "cost": 0}
    
    stats["total_usage"][service]["characters"] += characters
    stats["total_usage"][service]["cost"] += cost
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
EOF
```

## 🔐 安全建议

1. **API密钥安全**
   - 不要将API密钥提交到版本控制
   - 使用环境变量存储敏感信息
   - 定期轮换API密钥

2. **访问控制**
   ```bash
   # 设置配置文件权限
   chmod 600 translation_config.json
   
   # 创建.env文件存储密钥
   echo "TRANSLATION_API_KEY=your-key" > .env
   chmod 600 .env
   ```

3. **网络安全**
   - 使用HTTPS端点
   - 配置请求超时
   - 启用请求重试机制

## 📚 更多资源

- [DeepL API 文档](https://www.deepl.com/docs-api)
- [百度翻译API文档](https://fanyi-api.baidu.com/doc/21)
- [腾讯翻译API文档](https://cloud.tencent.com/document/product/551)
- [OpenAI API 文档](https://platform.openai.com/docs)

## 💡 最佳实践

1. **选择合适的翻译服务**
   - 个人用户：Google翻译（免费）
   - 质量要求高：DeepL
   - 国内用户：百度翻译
   - 企业用户：腾讯翻译或OpenAI

2. **优化翻译性能**
   - 启用缓存减少重复翻译
   - 批量处理提高效率
   - 设置合理的并发数

3. **控制翻译成本**
   - 监控API使用量
   - 设置每日使用限额
   - 优先翻译重要内容

---

如有问题，请参考故障排除部分或查看项目文档。
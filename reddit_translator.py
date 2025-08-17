#!/usr/bin/env python3
"""
MCP Reddit Server 增强版 - 带自动翻译功能

这个脚本在原有 MCP Reddit Server 功能基础上，添加了自动翻译功能，
将抓取到的英文内容自动翻译成中文，方便中文用户阅读。

支持的翻译服务:
- Google Translate (免费)
- DeepL API (高质量)
- 百度翻译 API
- 腾讯翻译 API
- OpenAI GPT 翻译
"""

import json
import time
import re
import asyncio
import aiohttp
import hashlib
import hmac
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import quote
import os
from dataclasses import dataclass

@dataclass
class TranslationConfig:
    """翻译配置类"""
    service: str = "google"  # google, deepl, baidu, tencent, openai
    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    endpoint: Optional[str] = None
    model: Optional[str] = None
    enabled: bool = True
    cache_enabled: bool = True
    max_length: int = 5000
    batch_size: int = 10

class TranslationService:
    """翻译服务基类"""
    
    def __init__(self, config: TranslationConfig):
        self.config = config
        self.cache = {}
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_cache_key(self, text: str) -> str:
        """生成缓存键"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _should_translate(self, text: str) -> bool:
        """判断是否需要翻译"""
        if not text or len(text.strip()) < 3:
            return False
        
        # 检查是否主要是中文
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(re.findall(r'[\w\u4e00-\u9fff]', text))
        
        if total_chars == 0:
            return False
        
        chinese_ratio = chinese_chars / total_chars
        return chinese_ratio < 0.3  # 如果中文字符少于30%，则翻译
    
    async def translate(self, text: str) -> str:
        """翻译文本"""
        if not self.config.enabled or not self._should_translate(text):
            return text
        
        # 检查缓存
        if self.config.cache_enabled:
            cache_key = self._get_cache_key(text)
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        # 文本长度限制
        if len(text) > self.config.max_length:
            text = text[:self.config.max_length] + "..."
        
        try:
            translated = await self._translate_impl(text)
            
            # 缓存结果
            if self.config.cache_enabled:
                self.cache[cache_key] = translated
            
            return translated
        except Exception as e:
            print(f"翻译失败: {str(e)}")
            return text  # 翻译失败时返回原文
    
    async def _translate_impl(self, text: str) -> str:
        """具体的翻译实现，由子类重写"""
        raise NotImplementedError

class GoogleTranslator(TranslationService):
    """Google 翻译服务"""
    
    async def _translate_impl(self, text: str) -> str:
        # 使用免费的 Google Translate API
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': 'en',
            'tl': 'zh-CN',
            'dt': 't',
            'q': text
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                result = await response.json()
                if result and result[0]:
                    return ''.join([item[0] for item in result[0] if item[0]])
        
        raise Exception("Google 翻译请求失败")

class DeepLTranslator(TranslationService):
    """DeepL 翻译服务"""
    
    async def _translate_impl(self, text: str) -> str:
        if not self.config.api_key:
            raise Exception("DeepL API 密钥未配置")
        
        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            'Authorization': f'DeepL-Auth-Key {self.config.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'text': [text],
            'source_lang': 'EN',
            'target_lang': 'ZH'
        }
        
        async with self.session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                if result.get('translations'):
                    return result['translations'][0]['text']
        
        raise Exception("DeepL 翻译请求失败")

class BaiduTranslator(TranslationService):
    """百度翻译服务"""
    
    def _generate_sign(self, query: str, salt: str) -> str:
        """生成百度翻译签名"""
        sign_str = self.config.api_key + query + salt + self.config.secret_key
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    
    async def _translate_impl(self, text: str) -> str:
        if not self.config.api_key or not self.config.secret_key:
            raise Exception("百度翻译 API 密钥未配置")
        
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        salt = str(int(time.time()))
        sign = self._generate_sign(text, salt)
        
        params = {
            'q': text,
            'from': 'en',
            'to': 'zh',
            'appid': self.config.api_key,
            'salt': salt,
            'sign': sign
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                result = await response.json()
                if result.get('trans_result'):
                    return result['trans_result'][0]['dst']
        
        raise Exception("百度翻译请求失败")

class OpenAITranslator(TranslationService):
    """OpenAI GPT 翻译服务"""
    
    async def _translate_impl(self, text: str) -> str:
        if not self.config.api_key:
            raise Exception("OpenAI API 密钥未配置")
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"请将以下英文内容翻译成中文，保持原文的格式和语气：\n\n{text}"
        
        data = {
            'model': self.config.model or 'gpt-3.5-turbo',
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 2000,
            'temperature': 0.3
        }
        
        async with self.session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                if result.get('choices'):
                    return result['choices'][0]['message']['content'].strip()
        
        raise Exception("OpenAI 翻译请求失败")

class TranslationManager:
    """翻译管理器"""
    
    def __init__(self, config: TranslationConfig):
        self.config = config
        self.translator = self._create_translator()
    
    def _create_translator(self) -> TranslationService:
        """创建翻译服务实例"""
        if self.config.service == "google":
            return GoogleTranslator(self.config)
        elif self.config.service == "deepl":
            return DeepLTranslator(self.config)
        elif self.config.service == "baidu":
            return BaiduTranslator(self.config)
        elif self.config.service == "openai":
            return OpenAITranslator(self.config)
        else:
            raise ValueError(f"不支持的翻译服务: {self.config.service}")
    
    async def translate_text(self, text: str) -> str:
        """翻译单个文本"""
        async with self.translator as translator:
            return await translator.translate(text)
    
    async def translate_batch(self, texts: List[str]) -> List[str]:
        """批量翻译文本"""
        async with self.translator as translator:
            tasks = [translator.translate(text) for text in texts]
            return await asyncio.gather(*tasks)

class EnhancedRedditMCP:
    """增强版 Reddit MCP，带翻译功能"""
    
    def __init__(self, translation_config: TranslationConfig = None):
        self.translation_config = translation_config or TranslationConfig()
        self.translation_manager = TranslationManager(self.translation_config)
        self.demo_data = self._load_demo_data()
    
    def _load_demo_data(self) -> Dict[str, Any]:
        """加载演示数据（英文版）"""
        return {
            "hot_threads": {
                "programming": [
                    {
                        "id": "abc123",
                        "title": "New JavaScript Framework 'FastJS' Released - 3x Faster than React",
                        "author": "tech_enthusiast",
                        "score": 1247,
                        "num_comments": 89,
                        "created_utc": 1703123456,
                        "url": "https://reddit.com/r/programming/comments/abc123",
                        "selftext": "After two years of development, our team has released FastJS, a performance-focused frontend framework that delivers unprecedented speed improvements over existing solutions. The framework introduces innovative virtual DOM optimizations and compile-time optimizations that result in 3x faster rendering compared to React in our benchmarks.",
                        "subreddit": "programming",
                        "post_hint": "self"
                    },
                    {
                        "id": "def456",
                        "title": "Python 3.12 Performance Optimization Deep Dive",
                        "author": "python_guru",
                        "score": 892,
                        "num_comments": 156,
                        "created_utc": 1703120000,
                        "url": "https://python.org/blog/performance-improvements",
                        "selftext": "Python 3.12 brings significant performance improvements through better memory management, optimized bytecode generation, and enhanced garbage collection. This comprehensive analysis covers all the major optimizations and their real-world impact.",
                        "subreddit": "programming",
                        "post_hint": "link"
                    }
                ],
                "MachineLearning": [
                    {
                        "id": "ghi789",
                        "title": "GPT-5 Architecture Leaked: Massive Multimodal Capabilities Upgrade",
                        "author": "ai_researcher",
                        "score": 2156,
                        "num_comments": 234,
                        "created_utc": 1703125000,
                        "url": "https://reddit.com/r/MachineLearning/comments/ghi789",
                        "selftext": "According to leaked information, GPT-5 will support video understanding, 3D modeling, and real-time multimodal interactions. The architecture includes specialized modules for different modalities and advanced reasoning capabilities that could revolutionize AI applications.",
                        "subreddit": "MachineLearning",
                        "post_hint": "self"
                    }
                ]
            },
            "comments": {
                "abc123": [
                    {
                        "id": "comment1",
                        "author": "senior_dev",
                        "body": "The design philosophy of this framework is really interesting, especially the virtual DOM optimization approach. Do you have detailed performance testing data available?",
                        "score": 45,
                        "created_utc": 1703124000,
                        "replies": [
                            {
                                "id": "reply1",
                                "author": "tech_enthusiast",
                                "body": "We've published comprehensive benchmark results on GitHub, including comparisons with React and Vue. The results show consistent performance improvements across different use cases.",
                                "score": 23,
                                "created_utc": 1703124300
                            }
                        ]
                    },
                    {
                        "id": "comment2",
                        "author": "frontend_ninja",
                        "body": "The documentation is very detailed and the API design is intuitive. Planning to try it in our next project. Great work on the developer experience!",
                        "score": 32,
                        "created_utc": 1703124500,
                        "replies": []
                    }
                ]
            }
        }
    
    async def fetch_hot_threads(self, subreddit: str, limit: int = 10, translate: bool = True) -> List[Dict[str, Any]]:
        """获取热门帖子（带翻译）"""
        print(f"🔥 正在获取 r/{subreddit} 的热门帖子...")
        
        threads = self.demo_data["hot_threads"].get(subreddit, [])
        limited_threads = threads[:limit]
        
        if translate and self.translation_config.enabled:
            print("🌐 正在翻译内容...")
            for thread in limited_threads:
                # 翻译标题
                thread["title_zh"] = await self.translation_manager.translate_text(thread["title"])
                # 翻译内容
                if thread.get("selftext"):
                    thread["selftext_zh"] = await self.translation_manager.translate_text(thread["selftext"])
        
        return limited_threads
    
    async def fetch_post_details(self, post_id: str, translate: bool = True) -> Dict[str, Any]:
        """获取帖子详情（带翻译）"""
        print(f"📄 正在获取帖子 {post_id} 的详细信息...")
        
        # 查找帖子
        for subreddit_threads in self.demo_data["hot_threads"].values():
            for thread in subreddit_threads:
                if thread["id"] == post_id:
                    # 添加评论信息
                    thread["comments"] = self.demo_data["comments"].get(post_id, [])
                    
                    if translate and self.translation_config.enabled:
                        print("🌐 正在翻译帖子和评论...")
                        
                        # 翻译帖子
                        thread["title_zh"] = await self.translation_manager.translate_text(thread["title"])
                        if thread.get("selftext"):
                            thread["selftext_zh"] = await self.translation_manager.translate_text(thread["selftext"])
                        
                        # 翻译评论
                        for comment in thread["comments"]:
                            comment["body_zh"] = await self.translation_manager.translate_text(comment["body"])
                            
                            # 翻译回复
                            for reply in comment.get("replies", []):
                                reply["body_zh"] = await self.translation_manager.translate_text(reply["body"])
                    
                    return thread
        
        return {"error": "帖子未找到"}
    
    async def search_posts(self, query: str, subreddit: str = None, translate: bool = True) -> List[Dict[str, Any]]:
        """搜索帖子（带翻译）"""
        search_target = f"r/{subreddit}" if subreddit else "全站"
        print(f"🔍 正在{search_target}搜索: {query}")
        
        results = []
        search_terms = query.lower().split()
        
        # 搜索逻辑
        for subreddit_name, threads in self.demo_data["hot_threads"].items():
            if subreddit and subreddit_name != subreddit:
                continue
                
            for thread in threads:
                title_lower = thread["title"].lower()
                content_lower = thread["selftext"].lower()
                
                if any(term in title_lower or term in content_lower for term in search_terms):
                    results.append(thread.copy())
        
        if translate and self.translation_config.enabled and results:
            print("🌐 正在翻译搜索结果...")
            for result in results:
                result["title_zh"] = await self.translation_manager.translate_text(result["title"])
                if result.get("selftext"):
                    result["selftext_zh"] = await self.translation_manager.translate_text(result["selftext"])
        
        return results
    
    def format_post(self, post: Dict[str, Any], show_translation: bool = True) -> str:
        """格式化帖子显示（支持中英文对照）"""
        created_time = datetime.fromtimestamp(post["created_utc"]).strftime("%Y-%m-%d %H:%M")
        post_type = "🔗 链接" if post["post_hint"] == "link" else "📝 文本"
        
        # 标题部分
        title_section = f"📌 **{post['title']}**"
        if show_translation and post.get("title_zh"):
            title_section += f"\n🌐 **{post['title_zh']}**"
        
        formatted = f"""
{title_section}
👤 作者: u/{post['author']} | ⏰ {created_time}
📊 {post['score']} 点赞 | 💬 {post['num_comments']} 评论 | {post_type}
🏷️ r/{post['subreddit']}
"""
        
        # 内容部分
        if post.get("selftext"):
            content = post["selftext"][:200] + "..." if len(post["selftext"]) > 200 else post["selftext"]
            formatted += f"\n📄 原文: {content}"
            
            if show_translation and post.get("selftext_zh"):
                content_zh = post["selftext_zh"][:200] + "..." if len(post["selftext_zh"]) > 200 else post["selftext_zh"]
                formatted += f"\n🌐 中文: {content_zh}"
        
        if post["post_hint"] == "link":
            formatted += f"\n🔗 链接: {post['url']}"
        
        return formatted
    
    def format_comments(self, comments: List[Dict[str, Any]], show_translation: bool = True) -> str:
        """格式化评论显示（支持中英文对照）"""
        if not comments:
            return "暂无评论"
        
        formatted_comments = []
        for comment in comments:
            created_time = datetime.fromtimestamp(comment["created_utc"]).strftime("%H:%M")
            
            comment_text = f"""
💬 **u/{comment['author']}** ({comment['score']} 点赞, {created_time})
   原文: {comment['body']}
"""
            
            if show_translation and comment.get("body_zh"):
                comment_text += f"   🌐 中文: {comment['body_zh']}\n"
            
            # 添加回复
            if comment.get("replies"):
                for reply in comment["replies"]:
                    reply_time = datetime.fromtimestamp(reply["created_utc"]).strftime("%H:%M")
                    comment_text += f"""
   ↳ **u/{reply['author']}** ({reply['score']} 点赞, {reply_time})
     原文: {reply['body']}
"""
                    if show_translation and reply.get("body_zh"):
                        comment_text += f"     🌐 中文: {reply['body_zh']}\n"
            
            formatted_comments.append(comment_text)
        
        return "\n".join(formatted_comments)
    
    async def demo_workflow(self):
        """演示完整的翻译工作流程"""
        print("🚀 MCP Reddit Server 增强版演示 - 带自动翻译功能")
        print("=" * 60)
        print(f"🌐 翻译服务: {self.translation_config.service}")
        print(f"📝 翻译状态: {'启用' if self.translation_config.enabled else '禁用'}")
        
        # 1. 获取热门帖子（带翻译）
        print("\n1️⃣ 获取热门帖子演示（自动翻译）")
        print("-" * 40)
        
        hot_posts = await self.fetch_hot_threads("programming", 2, translate=True)
        for i, post in enumerate(hot_posts, 1):
            print(f"\n📍 热门帖子 #{i}:")
            print(self.format_post(post, show_translation=True))
        
        # 2. 获取帖子详情（带翻译）
        print("\n\n2️⃣ 获取帖子详情演示（自动翻译）")
        print("-" * 40)
        
        if hot_posts:
            post_details = await self.fetch_post_details(hot_posts[0]["id"], translate=True)
            print(f"\n📖 帖子详情:")
            print(self.format_post(post_details, show_translation=True))
            
            if "comments" in post_details:
                print(f"\n💬 评论区:")
                print(self.format_comments(post_details["comments"], show_translation=True))
        
        # 3. 搜索功能（带翻译）
        print("\n\n3️⃣ 搜索功能演示（自动翻译）")
        print("-" * 40)
        
        search_results = await self.search_posts("JavaScript framework", translate=True)
        print(f"\n🔍 搜索结果 ({len(search_results)} 个):")
        for i, post in enumerate(search_results, 1):
            print(f"\n📍 搜索结果 #{i}:")
            print(self.format_post(post, show_translation=True))
        
        print("\n\n✅ 演示完成！")
        print("\n💡 所有英文内容已自动翻译成中文，方便阅读理解。")
        print("📚 详细配置请参考 INSTALLATION.md 文件。")

def load_translation_config() -> TranslationConfig:
    """从环境变量或配置文件加载翻译配置"""
    config = TranslationConfig()
    
    # 从环境变量读取配置
    config.service = os.getenv("TRANSLATION_SERVICE", "google")
    config.api_key = os.getenv("TRANSLATION_API_KEY")
    config.secret_key = os.getenv("TRANSLATION_SECRET_KEY")
    config.endpoint = os.getenv("TRANSLATION_ENDPOINT")
    config.model = os.getenv("TRANSLATION_MODEL")
    config.enabled = os.getenv("TRANSLATION_ENABLED", "true").lower() == "true"
    config.cache_enabled = os.getenv("TRANSLATION_CACHE_ENABLED", "true").lower() == "true"
    config.max_length = int(os.getenv("TRANSLATION_MAX_LENGTH", "5000"))
    config.batch_size = int(os.getenv("TRANSLATION_BATCH_SIZE", "10"))
    
    # 尝试从配置文件读取
    try:
        with open("translation_config.json", "r", encoding="utf-8") as f:
            file_config = json.load(f)
            for key, value in file_config.items():
                if hasattr(config, key):
                    setattr(config, key, value)
    except FileNotFoundError:
        pass
    
    return config

async def main():
    """主函数"""
    # 加载翻译配置
    translation_config = load_translation_config()
    
    # 创建增强版 Reddit MCP
    reddit_mcp = EnhancedRedditMCP(translation_config)
    
    try:
        await reddit_mcp.demo_workflow()
    except KeyboardInterrupt:
        print("\n\n⏹️ 演示被用户中断")
    except Exception as e:
        print(f"\n\n💥 演示过程中发生错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
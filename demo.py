#!/usr/bin/env python3
"""
MCP Reddit Server 功能演示脚本

这个脚本演示了如何使用 MCP Reddit Server 的各种功能，
包括模拟的 API 调用和响应格式。
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

class MCPRedditDemo:
    """MCP Reddit Server 功能演示类"""
    
    def __init__(self):
        self.demo_data = self._load_demo_data()
    
    def _load_demo_data(self) -> Dict[str, Any]:
        """加载演示数据"""
        return {
            "hot_threads": {
                "programming": [
                    {
                        "id": "abc123",
                        "title": "新的 JavaScript 框架 'FastJS' 发布 - 比 React 快 3 倍",
                        "author": "tech_enthusiast",
                        "score": 1247,
                        "num_comments": 89,
                        "created_utc": 1703123456,
                        "url": "https://reddit.com/r/programming/comments/abc123",
                        "selftext": "经过两年的开发，我们团队发布了 FastJS，一个专注于性能的前端框架...",
                        "subreddit": "programming",
                        "post_hint": "self"
                    },
                    {
                        "id": "def456",
                        "title": "Python 3.12 性能优化深度解析",
                        "author": "python_guru",
                        "score": 892,
                        "num_comments": 156,
                        "created_utc": 1703120000,
                        "url": "https://python.org/blog/performance-improvements",
                        "selftext": "",
                        "subreddit": "programming",
                        "post_hint": "link"
                    }
                ],
                "MachineLearning": [
                    {
                        "id": "ghi789",
                        "title": "GPT-5 架构泄露：多模态能力大幅提升",
                        "author": "ai_researcher",
                        "score": 2156,
                        "num_comments": 234,
                        "created_utc": 1703125000,
                        "url": "https://reddit.com/r/MachineLearning/comments/ghi789",
                        "selftext": "根据最新泄露的信息，GPT-5 将支持视频理解、3D 建模等功能...",
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
                        "body": "这个框架的设计理念很有趣，特别是虚拟 DOM 的优化方案。有没有性能测试的详细数据？",
                        "score": 45,
                        "created_utc": 1703124000,
                        "replies": [
                            {
                                "id": "reply1",
                                "author": "tech_enthusiast",
                                "body": "我们在 GitHub 上发布了完整的基准测试结果，包括与 React、Vue 的对比。",
                                "score": 23,
                                "created_utc": 1703124300
                            }
                        ]
                    },
                    {
                        "id": "comment2",
                        "author": "frontend_ninja",
                        "body": "文档写得很详细，API 设计也很直观。准备在下个项目中尝试一下。",
                        "score": 32,
                        "created_utc": 1703124500,
                        "replies": []
                    }
                ]
            }
        }
    
    def fetch_hot_threads(self, subreddit: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取热门帖子"""
        print(f"🔥 正在获取 r/{subreddit} 的热门帖子...")
        time.sleep(1)  # 模拟网络延迟
        
        threads = self.demo_data["hot_threads"].get(subreddit, [])
        return threads[:limit]
    
    def fetch_post_details(self, post_id: str) -> Dict[str, Any]:
        """获取帖子详情"""
        print(f"📄 正在获取帖子 {post_id} 的详细信息...")
        time.sleep(0.5)
        
        # 查找帖子
        for subreddit_threads in self.demo_data["hot_threads"].values():
            for thread in subreddit_threads:
                if thread["id"] == post_id:
                    # 添加评论信息
                    thread["comments"] = self.demo_data["comments"].get(post_id, [])
                    return thread
        
        return {"error": "帖子未找到"}
    
    def search_posts(self, query: str, subreddit: str = None) -> List[Dict[str, Any]]:
        """搜索帖子"""
        search_target = f"r/{subreddit}" if subreddit else "全站"
        print(f"🔍 正在{search_target}搜索: {query}")
        time.sleep(1)
        
        results = []
        search_terms = query.lower().split()
        
        # 搜索逻辑（简化版）
        for subreddit_name, threads in self.demo_data["hot_threads"].items():
            if subreddit and subreddit_name != subreddit:
                continue
                
            for thread in threads:
                title_lower = thread["title"].lower()
                content_lower = thread["selftext"].lower()
                
                # 检查是否包含搜索词
                if any(term in title_lower or term in content_lower for term in search_terms):
                    results.append(thread)
        
        return results
    
    def format_post(self, post: Dict[str, Any]) -> str:
        """格式化帖子显示"""
        created_time = datetime.fromtimestamp(post["created_utc"]).strftime("%Y-%m-%d %H:%M")
        
        post_type = "🔗 链接" if post["post_hint"] == "link" else "📝 文本"
        
        formatted = f"""
📌 **{post['title']}**
👤 作者: u/{post['author']} | ⏰ {created_time}
📊 {post['score']} 点赞 | 💬 {post['num_comments']} 评论 | {post_type}
🏷️ r/{post['subreddit']}
"""
        
        if post["selftext"]:
            content = post["selftext"][:200] + "..." if len(post["selftext"]) > 200 else post["selftext"]
            formatted += f"\n📄 内容: {content}"
        
        if post["post_hint"] == "link":
            formatted += f"\n🔗 链接: {post['url']}"
        
        return formatted
    
    def format_comments(self, comments: List[Dict[str, Any]]) -> str:
        """格式化评论显示"""
        if not comments:
            return "暂无评论"
        
        formatted_comments = []
        for comment in comments:
            created_time = datetime.fromtimestamp(comment["created_utc"]).strftime("%H:%M")
            
            comment_text = f"""
💬 **u/{comment['author']}** ({comment['score']} 点赞, {created_time})
   {comment['body']}
"""
            
            # 添加回复
            if comment.get("replies"):
                for reply in comment["replies"]:
                    reply_time = datetime.fromtimestamp(reply["created_utc"]).strftime("%H:%M")
                    comment_text += f"""
   ↳ **u/{reply['author']}** ({reply['score']} 点赞, {reply_time})
     {reply['body']}
"""
            
            formatted_comments.append(comment_text)
        
        return "\n".join(formatted_comments)
    
    def demo_workflow(self):
        """演示完整的工作流程"""
        print("🚀 MCP Reddit Server 功能演示")
        print("=" * 50)
        
        # 1. 获取热门帖子
        print("\n1️⃣ 获取热门帖子演示")
        print("-" * 30)
        
        hot_posts = self.fetch_hot_threads("programming", 2)
        for i, post in enumerate(hot_posts, 1):
            print(f"\n📍 热门帖子 #{i}:")
            print(self.format_post(post))
        
        # 2. 获取帖子详情
        print("\n\n2️⃣ 获取帖子详情演示")
        print("-" * 30)
        
        if hot_posts:
            post_details = self.fetch_post_details(hot_posts[0]["id"])
            print(f"\n📖 帖子详情:")
            print(self.format_post(post_details))
            
            if "comments" in post_details:
                print(f"\n💬 评论区:")
                print(self.format_comments(post_details["comments"]))
        
        # 3. 搜索功能
        print("\n\n3️⃣ 搜索功能演示")
        print("-" * 30)
        
        search_results = self.search_posts("JavaScript 框架")
        print(f"\n🔍 搜索结果 ({len(search_results)} 个):")
        for i, post in enumerate(search_results, 1):
            print(f"\n📍 搜索结果 #{i}:")
            print(self.format_post(post))
        
        # 4. 多 subreddit 演示
        print("\n\n4️⃣ 多 Subreddit 演示")
        print("-" * 30)
        
        subreddits = ["programming", "MachineLearning"]
        for subreddit in subreddits:
            posts = self.fetch_hot_threads(subreddit, 1)
            if posts:
                print(f"\n📍 r/{subreddit} 热门:")
                print(self.format_post(posts[0]))
        
        print("\n\n✅ 演示完成！")
        print("\n💡 实际使用时，这些功能将通过 MCP 协议与 AI 助手集成。")
        print("📚 详细配置请参考 INSTALLATION.md 文件。")

def main():
    """主函数"""
    demo = MCPRedditDemo()
    
    try:
        demo.demo_workflow()
    except KeyboardInterrupt:
        print("\n\n⏹️ 演示被用户中断")
    except Exception as e:
        print(f"\n\n💥 演示过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main()
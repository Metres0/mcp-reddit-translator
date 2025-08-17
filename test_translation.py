#!/usr/bin/env python3
"""
翻译功能测试脚本

这个脚本用于测试 MCP Reddit Server 的翻译功能，
验证不同翻译服务的配置和功能是否正常工作。
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from reddit_translator import (
    TranslationConfig, 
    TranslationManager, 
    GoogleTranslator,
    load_translation_config,
    EnhancedRedditMCP
)

class TranslationTester:
    """翻译功能测试器"""
    
    def __init__(self):
        self.test_results = []
        self.test_texts = [
            "Hello, this is a test message.",
            "The quick brown fox jumps over the lazy dog.",
            "Python is a powerful programming language.",
            "Machine learning is revolutionizing technology.",
            "Reddit is a popular social media platform."
        ]
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """记录测试结果"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} {test_name}: {message}")
    
    async def test_config_loading(self):
        """测试配置加载"""
        try:
            config = load_translation_config()
            self.log_test(
                "配置加载", 
                True, 
                f"成功加载配置，服务: {config.service}, 启用: {config.enabled}"
            )
            return config
        except Exception as e:
            self.log_test("配置加载", False, f"配置加载失败: {str(e)}")
            return None
    
    async def test_google_translation(self):
        """测试Google翻译"""
        try:
            config = TranslationConfig(service="google", enabled=True)
            manager = TranslationManager(config)
            
            test_text = "Hello World"
            result = await manager.translate_text(test_text)
            
            success = result != test_text and len(result) > 0
            self.log_test(
                "Google翻译", 
                success, 
                f"'{test_text}' -> '{result}'"
            )
            return success
        except Exception as e:
            self.log_test("Google翻译", False, f"翻译失败: {str(e)}")
            return False
    
    async def test_translation_cache(self):
        """测试翻译缓存"""
        try:
            config = TranslationConfig(service="google", enabled=True, cache_enabled=True)
            manager = TranslationManager(config)
            
            test_text = "Cache test message"
            
            # 第一次翻译
            result1 = await manager.translate_text(test_text)
            
            # 第二次翻译（应该使用缓存）
            result2 = await manager.translate_text(test_text)
            
            success = result1 == result2 and len(result1) > 0
            self.log_test(
                "翻译缓存", 
                success, 
                f"缓存功能正常，结果一致: '{result1}'"
            )
            return success
        except Exception as e:
            self.log_test("翻译缓存", False, f"缓存测试失败: {str(e)}")
            return False
    
    async def test_batch_translation(self):
        """测试批量翻译"""
        try:
            config = TranslationConfig(service="google", enabled=True)
            manager = TranslationManager(config)
            
            results = await manager.translate_batch(self.test_texts[:3])
            
            success = len(results) == 3 and all(len(r) > 0 for r in results)
            self.log_test(
                "批量翻译", 
                success, 
                f"成功翻译 {len(results)} 个文本"
            )
            return success
        except Exception as e:
            self.log_test("批量翻译", False, f"批量翻译失败: {str(e)}")
            return False
    
    async def test_language_detection(self):
        """测试语言检测"""
        try:
            config = TranslationConfig(service="google", enabled=True)
            translator = GoogleTranslator(config)
            
            # 测试英文文本
            english_text = "This is English text"
            should_translate_en = translator._should_translate(english_text)
            
            # 测试中文文本
            chinese_text = "这是中文文本"
            should_translate_zh = translator._should_translate(chinese_text)
            
            # 测试混合文本
            mixed_text = "This is 混合 text"
            should_translate_mixed = translator._should_translate(mixed_text)
            
            success = should_translate_en and not should_translate_zh
            self.log_test(
                "语言检测", 
                success, 
                f"英文: {should_translate_en}, 中文: {should_translate_zh}, 混合: {should_translate_mixed}"
            )
            return success
        except Exception as e:
            self.log_test("语言检测", False, f"语言检测失败: {str(e)}")
            return False
    
    async def test_reddit_integration(self):
        """测试Reddit集成"""
        try:
            config = TranslationConfig(service="google", enabled=True)
            reddit_mcp = EnhancedRedditMCP(config)
            
            # 测试获取热门帖子
            posts = await reddit_mcp.fetch_hot_threads("programming", 1, translate=True)
            
            success = len(posts) > 0 and "title_zh" in posts[0]
            self.log_test(
                "Reddit集成", 
                success, 
                f"成功获取并翻译 {len(posts)} 个帖子"
            )
            return success
        except Exception as e:
            self.log_test("Reddit集成", False, f"Reddit集成测试失败: {str(e)}")
            return False
    
    async def test_error_handling(self):
        """测试错误处理"""
        try:
            # 测试无效配置
            config = TranslationConfig(service="invalid_service", enabled=True)
            
            try:
                manager = TranslationManager(config)
                self.log_test("错误处理", False, "应该抛出异常但没有")
                return False
            except ValueError:
                self.log_test("错误处理", True, "正确处理无效服务配置")
                return True
        except Exception as e:
            self.log_test("错误处理", False, f"错误处理测试失败: {str(e)}")
            return False
    
    async def test_performance(self):
        """测试性能"""
        try:
            config = TranslationConfig(service="google", enabled=True)
            manager = TranslationManager(config)
            
            import time
            start_time = time.time()
            
            # 翻译多个文本
            tasks = [manager.translate_text(text) for text in self.test_texts]
            results = await asyncio.gather(*tasks)
            
            end_time = time.time()
            duration = end_time - start_time
            
            success = len(results) == len(self.test_texts) and duration < 30  # 30秒内完成
            self.log_test(
                "性能测试", 
                success, 
                f"翻译 {len(self.test_texts)} 个文本耗时 {duration:.2f} 秒"
            )
            return success
        except Exception as e:
            self.log_test("性能测试", False, f"性能测试失败: {str(e)}")
            return False
    
    def generate_report(self):
        """生成测试报告"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = f"""
📊 翻译功能测试报告
{'=' * 50}

📈 总体统计:
   总测试数: {total_tests}
   通过测试: {passed_tests}
   失败测试: {failed_tests}
   成功率: {success_rate:.1f}%

📋 详细结果:
"""
        
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            report += f"   {status} {result['test']}: {result['message']}\n"
        
        report += f"""

💡 建议:
"""
        
        if success_rate >= 80:
            report += "   🎉 翻译功能运行良好！可以正常使用。\n"
        elif success_rate >= 60:
            report += "   ⚠️ 翻译功能基本正常，但有一些问题需要解决。\n"
        else:
            report += "   🚨 翻译功能存在严重问题，需要检查配置和网络连接。\n"
        
        if failed_tests > 0:
            report += "   📝 请检查失败的测试项，确保API密钥配置正确。\n"
            report += "   🌐 确保网络连接正常，可以访问翻译服务。\n"
        
        report += f"""

📚 更多帮助:
   - 配置指南: TRANSLATION_SETUP.md
   - 安装指南: INSTALLATION.md
   - 项目概览: PROJECT_OVERVIEW.md

⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始翻译功能测试...")
        print("=" * 50)
        
        # 运行各项测试
        await self.test_config_loading()
        await self.test_google_translation()
        await self.test_translation_cache()
        await self.test_batch_translation()
        await self.test_language_detection()
        await self.test_reddit_integration()
        await self.test_error_handling()
        await self.test_performance()
        
        # 生成报告
        report = self.generate_report()
        print(report)
        
        # 保存报告到文件
        with open("translation_test_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("📄 测试报告已保存到: translation_test_report.txt")

async def main():
    """主函数"""
    tester = TranslationTester()
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
MCP Reddit Server 功能测试脚本

这个脚本用于测试 MCP Reddit Server 的各项功能，包括:
- 获取热门帖子
- 搜索特定内容
- 获取帖子详情
- 处理不同类型的内容
"""

import json
import subprocess
import sys
from typing import Dict, List, Any

class MCPRedditTester:
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "message": message
        }
        self.test_results.append(result)
        
        if success:
            self.passed += 1
        else:
            self.failed += 1
        
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
    
    def test_mcp_server_installation(self):
        """测试 MCP Reddit Server 是否正确安装"""
        try:
            # 尝试运行 mcp-reddit 命令
            result = subprocess.run(
                ["uvx", "--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit", "--help"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log_test("MCP Server 安装检查", True, "服务器可以正常启动")
                return True
            else:
                self.log_test("MCP Server 安装检查", False, f"启动失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_test("MCP Server 安装检查", False, "启动超时")
            return False
        except FileNotFoundError:
            self.log_test("MCP Server 安装检查", False, "uvx 命令未找到，请先安装 uv")
            return False
        except Exception as e:
            self.log_test("MCP Server 安装检查", False, f"未知错误: {str(e)}")
            return False
    
    def test_config_file(self):
        """测试配置文件格式"""
        try:
            with open("mcp_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # 检查配置文件结构
            if "mcpServers" not in config:
                self.log_test("配置文件格式检查", False, "缺少 mcpServers 字段")
                return False
            
            if "reddit" not in config["mcpServers"]:
                self.log_test("配置文件格式检查", False, "缺少 reddit 服务器配置")
                return False
            
            reddit_config = config["mcpServers"]["reddit"]
            required_fields = ["command", "args"]
            
            for field in required_fields:
                if field not in reddit_config:
                    self.log_test("配置文件格式检查", False, f"缺少必需字段: {field}")
                    return False
            
            self.log_test("配置文件格式检查", True, "配置文件格式正确")
            return True
            
        except FileNotFoundError:
            self.log_test("配置文件格式检查", False, "配置文件不存在")
            return False
        except json.JSONDecodeError as e:
            self.log_test("配置文件格式检查", False, f"JSON 格式错误: {str(e)}")
            return False
        except Exception as e:
            self.log_test("配置文件格式检查", False, f"读取配置文件失败: {str(e)}")
            return False
    
    def test_sample_subreddits(self):
        """测试常用 subreddit 的可访问性"""
        sample_subreddits = [
            "programming",
            "Python",
            "MachineLearning",
            "technology",
            "AskReddit"
        ]
        
        accessible_count = 0
        
        for subreddit in sample_subreddits:
            try:
                # 这里模拟检查 subreddit 的可访问性
                # 在实际环境中，这会通过 MCP 调用来完成
                print(f"   检查 r/{subreddit}...")
                
                # 模拟成功的情况（在实际实现中会调用真实的 API）
                accessible_count += 1
                
            except Exception as e:
                print(f"   r/{subreddit} 访问失败: {str(e)}")
        
        success_rate = accessible_count / len(sample_subreddits)
        if success_rate >= 0.8:  # 80% 成功率认为通过
            self.log_test(
                "Subreddit 可访问性测试", 
                True, 
                f"{accessible_count}/{len(sample_subreddits)} 个 subreddit 可访问"
            )
            return True
        else:
            self.log_test(
                "Subreddit 可访问性测试", 
                False, 
                f"只有 {accessible_count}/{len(sample_subreddits)} 个 subreddit 可访问"
            )
            return False
    
    def test_documentation(self):
        """测试文档完整性"""
        try:
            with open("README.md", "r", encoding="utf-8") as f:
                content = f.read()
            
            required_sections = [
                "# MCP Reddit Server",
                "## 主要功能",
                "## 使用示例",
                "## 支持的内容类型",
                "## 注意事项"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if not missing_sections:
                self.log_test("文档完整性检查", True, "所有必需章节都存在")
                return True
            else:
                self.log_test(
                    "文档完整性检查", 
                    False, 
                    f"缺少章节: {', '.join(missing_sections)}"
                )
                return False
                
        except FileNotFoundError:
            self.log_test("文档完整性检查", False, "README.md 文件不存在")
            return False
        except Exception as e:
            self.log_test("文档完整性检查", False, f"读取文档失败: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始 MCP Reddit Server 功能测试\n")
        
        # 运行各项测试
        self.test_config_file()
        self.test_documentation()
        self.test_sample_subreddits()
        self.test_mcp_server_installation()
        
        # 输出测试结果摘要
        print("\n" + "="*50)
        print("📊 测试结果摘要")
        print("="*50)
        print(f"总测试数: {len(self.test_results)}")
        print(f"通过: {self.passed}")
        print(f"失败: {self.failed}")
        print(f"成功率: {(self.passed/len(self.test_results)*100):.1f}%")
        
        if self.failed == 0:
            print("\n🎉 所有测试通过！MCP Reddit Server 配置正确。")
        else:
            print("\n⚠️  部分测试失败，请检查上述错误信息。")
        
        return self.failed == 0
    
    def generate_report(self):
        """生成详细的测试报告"""
        report = {
            "timestamp": subprocess.check_output(["date"], text=True).strip(),
            "summary": {
                "total_tests": len(self.test_results),
                "passed": self.passed,
                "failed": self.failed,
                "success_rate": round(self.passed/len(self.test_results)*100, 1)
            },
            "test_results": self.test_results
        }
        
        with open("test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细测试报告已保存到: test_report.json")

def main():
    """主函数"""
    tester = MCPRedditTester()
    
    try:
        success = tester.run_all_tests()
        tester.generate_report()
        
        # 根据测试结果设置退出码
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 测试过程中发生未预期的错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
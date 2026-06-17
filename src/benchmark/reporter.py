"""
基准测试报告生成器

生成HTML、JSON、文本格式的性能报告，支持可视化图表。
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import asdict
import matplotlib.pyplot as plt
import numpy as np
from .runner import BenchmarkResult


class BenchmarkReporter:
    """基准测试报告生成器"""
    
    def __init__(self, output_dir: str = "benchmark_reports"):
        """
        初始化报告生成器
        
        Args:
            output_dir: 报告输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_text_report(
        self,
        results: List[BenchmarkResult],
        title: str = "基准测试报告"
    ) -> str:
        """
        生成文本格式报告
        
        Args:
            results: 基准测试结果列表
            title: 报告标题
            
        Returns:
            str: 文本报告
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append(title)
        report_lines.append("=" * 80)
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"测试数量: {len(results)}")
        report_lines.append("")
        
        # 按执行时间排序
        sorted_results = sorted(
            results,
            key=lambda r: r.statistics.get("time_mean", 0),
            reverse=True
        )
        
        # 详细结果
        for i, result in enumerate(sorted_results, 1):
            stats = result.statistics
            report_lines.append(f"{i}. {result.name}")
            report_lines.append(f"   函数: {result.function_name}")
            report_lines.append(f"   执行时间: {stats.get('time_mean', 0):.6f}s ± {stats.get('time_std', 0):.6f}s")
            report_lines.append(f"   内存使用: {stats.get('memory_mean', 0) / 1024:.2f}KB ± {stats.get('memory_std', 0) / 1024:.2f}KB")
            if "cpu_mean" in stats:
                report_lines.append(f"   CPU使用率: {stats.get('cpu_mean', 0):.2f}% ± {stats.get('cpu_std', 0):.2f}%")
            report_lines.append(f"   测试次数: {len(result.execution_times)}")
            report_lines.append(f"   时间戳: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
        
        # 统计摘要
        if len(results) > 1:
            report_lines.append("统计摘要:")
            report_lines.append("-" * 80)
            
            # 最快和最慢
            fastest = min(results, key=lambda r: r.statistics.get("time_mean", float('inf')))
            slowest = max(results, key=lambda r: r.statistics.get("time_mean", 0))
            
            report_lines.append(f"最快测试: {fastest.name} ({fastest.statistics.get('time_mean', 0):.6f}s)")
            report_lines.append(f"最慢测试: {slowest.name} ({slowest.statistics.get('time_mean', 0):.6f}s)")
            
            # 内存使用
            min_memory = min(results, key=lambda r: r.statistics.get("memory_mean", float('inf')))
            max_memory = max(results, key=lambda r: r.statistics.get("memory_mean", 0))
            
            report_lines.append(f"最少内存: {min_memory.name} ({min_memory.statistics.get('memory_mean', 0) / 1024:.2f}KB)")
            report_lines.append(f"最多内存: {max_memory.name} ({max_memory.statistics.get('memory_mean', 0) / 1024:.2f}KB)")
            
            # 总体统计
            total_time = sum(r.statistics.get("time_mean", 0) for r in results)
            avg_time = total_time / len(results)
            total_memory = sum(r.statistics.get("memory_mean", 0) for r in results)
            avg_memory = total_memory / len(results)
            
            report_lines.append(f"平均执行时间: {avg_time:.6f}s")
            report_lines.append(f"平均内存使用: {avg_memory / 1024:.2f}KB")
        
        report_lines.append("=" * 80)
        return '\n'.join(report_lines)
    
    def generate_html_report(
        self,
        results: List[BenchmarkResult],
        title: str = "基准测试报告",
        include_charts: bool = True
    ) -> str:
        """
        生成HTML格式报告
        
        Args:
            results: 基准测试结果列表
            title: 报告标题
            include_charts: 是否包含图表
            
        Returns:
            str: HTML报告
        """
        # 按执行时间排序
        sorted_results = sorted(
            results,
            key=lambda r: r.statistics.get("time_mean", 0),
            reverse=True
        )
        
        # 生成图表数据
        chart_data = ""
        if include_charts and results:
            chart_data = self._generate_chart_data(sorted_results)
        
        # 生成HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .result-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        .result-table th, .result-table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        .result-table th {{
            background-color: #4CAF50;
            color: white;
        }}
        .result-table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .result-table tr:hover {{
            background-color: #f1f1f1;
        }}
        .chart-container {{
            margin: 30px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        .stat-box {{
            display: inline-block;
            background-color: #e8f5e9;
            padding: 15px;
            margin: 10px;
            border-radius: 5px;
            min-width: 200px;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        }}
        .stat-label {{
            font-size: 14px;
            color: #666;
        }}
        .timestamp {{
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <div class="summary">
            <h2>测试概览</h2>
            <div class="stat-box">
                <div class="stat-value">{len(results)}</div>
                <div class="stat-label">测试数量</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{sum(len(r.execution_times) for r in results)}</div>
                <div class="stat-label">总迭代次数</div>
            </div>
        </div>
        
        <h2>详细结果</h2>
        <table class="result-table">
            <thead>
                <tr>
                    <th>测试名称</th>
                    <th>函数名</th>
                    <th>平均时间 (s)</th>
                    <th>标准差 (s)</th>
                    <th>平均内存 (KB)</th>
                    <th>测试次数</th>
                    <th>时间戳</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in sorted_results:
            stats = result.statistics
            html += f"""                <tr>
                    <td>{result.name}</td>
                    <td>{result.function_name}</td>
                    <td>{stats.get('time_mean', 0):.6f}</td>
                    <td>{stats.get('time_std', 0):.6f}</td>
                    <td>{stats.get('memory_mean', 0) / 1024:.2f}</td>
                    <td>{len(result.execution_times)}</td>
                    <td>{result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</td>
                </tr>
"""
        
        html += """            </tbody>
        </table>
        
"""
        
        if include_charts and results:
            html += f"""        <div class="chart-container">
            <h2>性能对比图表</h2>
            <canvas id="performanceChart" width="800" height="400"></canvas>
        </div>
        
        <script>
            {chart_data}
            
            // 创建图表
            const ctx = document.getElementById('performanceChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: benchmarkNames,
                    datasets: [
                        {{
                            label: '平均执行时间 (秒)',
                            data: timeData,
                            backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }},
                        {{
                            label: '平均内存使用 (KB)',
                            data: memoryData,
                            backgroundColor: 'rgba(255, 99, 132, 0.5)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            yAxisID: 'y1'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: '执行时间 (秒)'
                            }}
                        }},
                        y1: {{
                            position: 'right',
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: '内存使用 (KB)'
                            }},
                            grid: {{
                                drawOnChartArea: false
                            }}
                        }}
                    }},
                    plugins: {{
                        title: {{
                            display: true,
                            text: '基准测试性能对比'
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    let label = context.dataset.label || '';
                                    if (label) {{
                                        label += ': ';
                                    }}
                                    if (context.datasetIndex === 0) {{
                                        label += context.parsed.y.toFixed(6) + 's';
                                    }} else {{
                                        label += context.parsed.y.toFixed(2) + 'KB';
                                    }}
                                    return label;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        </script>
"""
        
        html += """    </div>
</body>
</html>"""
        
        return html
    
    def _generate_chart_data(self, results: List[BenchmarkResult]) -> str:
        """生成图表数据"""
        benchmark_names = []
        time_data = []
        memory_data = []
        cpu_data = []
        
        for result in results:
            benchmark_names.append(f'"{result.name}"')
            stats = result.statistics
            time_data.append(stats.get("time_mean", 0))
            memory_data.append(stats.get("memory_mean", 0) / 1024)  # 转换为KB
            if "cpu_mean" in stats:
                cpu_data.append(stats.get("cpu_mean", 0))
        
        chart_data = f"""
            // 图表数据
            const benchmarkNames = [{', '.join(benchmark_names)}];
            const timeData = [{', '.join(f'{t:.6f}' for t in time_data)}];
            const memoryData = [{', '.join(f'{m:.2f}' for m in memory_data)}];
        """
        
        if cpu_data:
            chart_data += f"""
            const cpuData = [{', '.join(f'{c:.2f}' for c in cpu_data)}];
            """
        
        return chart_data
    
    def generate_json_report(
        self,
        results: List[BenchmarkResult],
        title: str = "基准测试报告"
    ) -> Dict[str, Any]:
        """
        生成JSON格式报告
        
        Args:
            results: 基准测试结果列表
            title: 报告标题
            
        Returns:
            Dict[str, Any]: JSON报告数据
        """
        report_data = {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "total_tests": len(results),
            "results": [],
            "summary": {}
        }
        
        # 添加详细结果
        for result in results:
            result_dict = result.to_dict()
            report_data["results"].append(result_dict)
        
        # 添加统计摘要
        if results:
            report_data["summary"] = {
                "fastest_test": min(results, key=lambda r: r.statistics.get("time_mean", float('inf'))).name,
                "slowest_test": max(results, key=lambda r: r.statistics.get("time_mean", 0)).name,
                "min_memory_test": min(results, key=lambda r: r.statistics.get("memory_mean", float('inf'))).name,
                "max_memory_test": max(results, key=lambda r: r.statistics.get("memory_mean", 0)).name,
                "average_time": sum(r.statistics.get("time_mean", 0) for r in results) / len(results),
                "average_memory": sum(r.statistics.get("memory_mean", 0) for r in results) / len(results),
                "total_iterations": sum(len(r.execution_times) for r in results),
            }
        
        return report_data
    
    def save_report(
        self,
        results: List[BenchmarkResult],
        title: str = "基准测试报告",
        formats: List[str] = None
    ) -> Dict[str, str]:
        """
        保存报告到文件
        
        Args:
            results: 基准测试结果列表
            title: 报告标题
            formats: 报告格式列表，支持['txt', 'html', 'json']
            
        Returns:
            Dict[str, str]: 文件路径字典
        """
        if formats is None:
            formats = ['txt', 'html', 'json']
        
        filepaths = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"benchmark_report_{timestamp}"
        
        # 生成文本报告
        if 'txt' in formats:
            txt_report = self.generate_text_report(results, title)
            txt_path = os.path.join(self.output_dir, f"{base_filename}.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(txt_report)
            filepaths['txt'] = txt_path
        
        # 生成HTML报告
        if 'html' in formats:
            html_report = self.generate_html_report(results, title)
            html_path = os.path.join(self.output_dir, f"{base_filename}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_report)
            filepaths['html'] = html_path
        
        # 生成JSON报告
        if 'json' in formats:
            json_report = self.generate_json_report(results, title)
            json_path = os.path.join(self.output_dir, f"{base_filename}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_report, f, indent=2, default=str)
            filepaths['json'] = json_path
        
        return filepaths
    
    def generate_comparison_report(
        self,
        baseline_results: List[BenchmarkResult],
        current_results: List[BenchmarkResult],
        title: str = "性能对比报告"
    ) -> str:
        """
        生成性能对比报告
        
        Args:
            baseline_results: 基准线结果
            current_results: 当前结果
            title: 报告标题
            
        Returns:
            str: 对比报告
        """
        # 创建结果映射
        baseline_map = {r.name: r for r in baseline_results}
        current_map = {r.name: r for r in current_results}
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append(title)
        report_lines.append("=" * 80)
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # 对比每个测试
        all_tests = set(baseline_map.keys()) | set(current_map.keys())
        
        for test_name in sorted(all_tests):
            report_lines.append(f"测试: {test_name}")
            report_lines.append("-" * 40)
            
            if test_name in baseline_map and test_name in current_map:
                baseline = baseline_map[test_name]
                current = current_map[test_name]
                
                baseline_time = baseline.statistics.get("time_mean", 0)
                current_time = current.statistics.get("time_mean", 0)
                
                baseline_memory = baseline.statistics.get("memory_mean", 0)
                current_memory = current.statistics.get("memory_mean", 0)
                
                # 计算变化
                time_change = ((current_time - baseline_time) / baseline_time * 100) if baseline_time > 0 else 0
                memory_change = ((current_memory - baseline_memory) / baseline_memory * 100) if baseline_memory > 0 else 0
                
                report_lines.append(f"  执行时间: {baseline_time:.6f}s -> {current_time:.6f}s ({time_change:+.2f}%)")
                report_lines.append(f"  内存使用: {baseline_memory / 1024:.2f}KB -> {current_memory / 1024:.2f}KB ({memory_change:+.2f}%)")
                
                if time_change > 5:
                    report_lines.append("  ⚠️  性能下降超过5%")
                elif time_change < -5:
                    report_lines.append("  ✅  性能提升超过5%")
                else:
                    report_lines.append("  ➡️  性能变化在5%以内")
                    
            elif test_name in baseline_map:
                report_lines.append("  ❌ 当前版本中缺少此测试")
            else:
                report_lines.append("  ➕ 基准线中缺少此测试")
            
            report_lines.append("")
        
        report_lines.append("=" * 80)
        return '\n'.join(report_lines)
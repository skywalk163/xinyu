#!/usr/bin/env python3
"""
简单测试算法实现
"""

import http.server
import socketserver
import threading
import time
import urllib.request
import urllib.parse
import json

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 读取index.html
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            self.wfile.write(content.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/run':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            code = data.get('code', '')
            
            # 简单的心语解释器（仅用于测试）
            output = self.simulate_xinyu_execution(code)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            response = json.dumps({'output': output})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def simulate_xinyu_execution(self, code):
        """简单模拟心语代码执行"""
        output_lines = []
        
        # 检查是否是汉诺塔算法
        if "汉诺塔问题" in code:
            output_lines.append("汉诺塔问题求解")
            output_lines.append("==================")
            output_lines.append("")
            output_lines.append("汉诺塔递归公式：移动次数 = 2^n - 1")
            output_lines.append("")
            output_lines.append("计算1到5个盘子的移动次数：")
            for n in range(1, 6):
                moves = (1 << n) - 1  # 2^n - 1
                output_lines.append(f"{n}个盘子需要{moves}步移动")
            output_lines.append("")
            output_lines.append("3个盘子的移动步骤（通过算法计算）：")
            output_lines.append("")
            output_lines.append("第1步：移动盘子1 从A到C")
            output_lines.append("第2步：移动盘子2 从A到B")
            output_lines.append("第3步：移动盘子1 从C到B")
            output_lines.append("第4步：移动盘子3 从A到C")
            output_lines.append("第5步：移动盘子1 从B到A")
            output_lines.append("第6步：移动盘子2 从B到C")
            output_lines.append("第7步：移动盘子1 从A到C")
            output_lines.append("")
            output_lines.append("总共需要7步完成。")
        
        # 检查是否是冒泡排序算法
        elif "冒泡排序算法" in code:
            output_lines.append("冒泡排序算法")
            output_lines.append("==============")
            output_lines.append("")
            output_lines.append("原始数组：[64, 34, 25, 12, 22, 11, 90]")
            output_lines.append("")
            output_lines.append("开始排序...")
            output_lines.append("第1轮排序：[34, 25, 12, 22, 11, 64, 90]")
            output_lines.append("第2轮排序：[25, 12, 22, 11, 34, 64, 90]")
            output_lines.append("第3轮排序：[12, 22, 11, 25, 34, 64, 90]")
            output_lines.append("第4轮排序：[12, 11, 22, 25, 34, 64, 90]")
            output_lines.append("第5轮排序：[11, 12, 22, 25, 34, 64, 90]")
            output_lines.append("")
            output_lines.append("排序完成！")
            output_lines.append("最终结果：[11, 12, 22, 25, 34, 64, 90]")
            output_lines.append("")
            output_lines.append("算法分析：")
            output_lines.append("时间复杂度：O(n的平方)")
            output_lines.append("空间复杂度：O(1)")
            output_lines.append("稳定排序：是")
            output_lines.append("原地排序：是")
        
        # 检查是否是图灵机算法
        elif "图灵机模拟" in code:
            output_lines.append("图灵机：二进制加1")
            output_lines.append("==================")
            output_lines.append("")
            output_lines.append("算法步骤：")
            output_lines.append("1. 从最右端开始")
            output_lines.append("2. 如果当前位是0，改为1，停止")
            output_lines.append("3. 如果当前位是1，改为0，左移一位")
            output_lines.append("4. 重复步骤2-3直到停止")
            output_lines.append("")
            output_lines.append("模拟二进制 1011 + 1：")
            output_lines.append("输入：1011")
            output_lines.append("")
            output_lines.append("步骤1：最右位是1，改为0，进位1")
            output_lines.append("步骤2：右数第二位是1，改为0，进位1")
            output_lines.append("步骤3：右数第三位是0，改为1，停止")
            output_lines.append("")
            output_lines.append("最终结果：1100")
            output_lines.append("")
            output_lines.append("验证：1011(二进制) = 11(十进制)")
            output_lines.append("       1100(二进制) = 12(十进制)")
            output_lines.append("       11 + 1 = 12 正确")
            output_lines.append("")
            output_lines.append("图灵机特点：")
            output_lines.append("1. 无限纸带")
            output_lines.append("2. 读写头")
            output_lines.append("3. 状态转移规则")
            output_lines.append("4. 计算通用性")
        
        # 检查是否是素数筛算法
        elif "埃拉托斯特尼素数筛" in code:
            output_lines.append("埃拉托斯特尼素数筛")
            output_lines.append("==================")
            output_lines.append("")
            output_lines.append("算法原理：")
            output_lines.append("1. 创建从2到n的整数列表")
            output_lines.append("2. 第一个数2是素数，标记其所有倍数为合数")
            output_lines.append("3. 找到下一个未被标记的数，标记其所有倍数")
            output_lines.append("4. 重复步骤3直到√n")
            output_lines.append("5. 剩下的未被标记的数就是素数")
            output_lines.append("")
            output_lines.append("筛选2到30之间的素数：")
            output_lines.append("")
            output_lines.append("第1步：2是素数，标记2的倍数")
            output_lines.append("标记的倍数：[4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]")
            output_lines.append("")
            output_lines.append("第2步：3是素数，标记3的倍数")
            output_lines.append("标记的倍数：[6, 9, 12, 15, 18, 21, 24, 27, 30]")
            output_lines.append("")
            output_lines.append("第3步：5是素数，标记5的倍数")
            output_lines.append("标记的倍数：[10, 15, 20, 25, 30]")
            output_lines.append("")
            output_lines.append("第4步：7是素数，标记7的倍数")
            output_lines.append("标记的倍数：[14, 21, 28]")
            output_lines.append("")
            output_lines.append("筛选完成，剩下的素数是：")
            output_lines.append("[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]")
            output_lines.append("")
            output_lines.append("共找到10个素数。")
            output_lines.append("")
            output_lines.append("算法复杂度：")
            output_lines.append("时间：O(n log log n)")
            output_lines.append("空间：O(n)")
        
        else:
            output_lines.append("测试输出：代码执行成功")
            output_lines.append("这是一个测试响应，实际代码会在浏览器中执行")
        
        return "\n".join(output_lines)

def start_test_server(port=5002):
    """启动测试服务器"""
    handler = TestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"测试服务器启动在 http://localhost:{port}")
        print("按 Ctrl+C 停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    print("启动测试服务器...")
    start_test_server(5002)
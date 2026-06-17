#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""心语 Playground 后端服务

提供在线代码执行API
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """返回playground主页"""
    return send_from_directory('.', 'index.html')


@app.route('/api/execute', methods=['POST'])
def execute():
    """执行心语代码"""
    try:
        data = request.get_json()
        code = data.get('code', '')

        if not code:
            return jsonify({
                'success': False,
                'error': '代码不能为空'
            })

        # 编译心语代码
        output_lines = []

        try:
            # 词法分析
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            # 语法分析
            parser = Parser(tokens)
            ast = parser.parse()

            # 代码生成
            codegen = PythonCodegen()
            python_code = codegen.generate(ast)

            # 执行生成的Python代码
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()

            try:
                # 创建执行环境，包含所有内置函数
                import builtins
                exec_globals = {
                    '__name__': '__main__',
                    '__builtins__': builtins,
                    # 添加常用的内置函数
                    'print': print,
                    'len': len,
                    'range': range,
                    'list': list,
                    'dict': dict,
                    'str': str,
                    'int': int,
                    'float': float,
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'sorted': sorted,
                    'type': type,
                }

                # 执行代码
                exec(python_code, exec_globals)

                # 获取输出
                stdout_value = sys.stdout.getvalue()
                stderr_value = sys.stderr.getvalue()

                if stdout_value:
                    output_lines.extend(stdout_value.strip().split('\n'))
                if stderr_value:
                    output_lines.append(f'[ERROR] {stderr_value.strip()}')

            except Exception as e:
                output_lines.append(f'[ERROR] 执行错误: {str(e)}')
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

            return jsonify({
                'success': True,
                'output': output_lines,
                'python_code': python_code
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'编译错误: {str(e)}'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        })


@app.route('/api/compile', methods=['POST'])
def compile():
    """编译心语代码为Python代码（不执行）"""
    try:
        data = request.get_json()
        code = data.get('code', '')

        if not code:
            return jsonify({
                'success': False,
                'error': '代码不能为空'
            })

        # 编译心语代码
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        codegen = PythonCodegen()
        python_code = codegen.generate(ast)

        return jsonify({
            'success': True,
            'python_code': python_code
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("=" * 60)
    print("心语 Playground 服务器")
    print("=" * 60)
    print()
    print("访问地址: http://localhost:5000")
    print()
    print("功能:")
    print("  - 在线编写和执行心语代码")
    print("  - 查看语法文档")
    print("  - 加载示例代码")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=True)

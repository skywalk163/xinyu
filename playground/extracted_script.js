
        const examples = {
            hello: `# 你好，世界
定义 问候 = "你好，心语！"。
打印 问候。

定义 名字 = "世界"。
打印 "你好，" 名字。`,

            variables: `# 变量定义示例
定义 整数 = 42。
定义 浮点数 = 3.14。
定义 字符串 = "心语"。
定义 布尔值 = True。

打印 "整数：" 整数。
打印 "浮点数：" 浮点数。
打印 "字符串：" 字符串。
打印 "布尔值：" 布尔值。`,

            function: `# 函数定义示例
定义 平方 = 函 x：
  返回 x 相乘 x。
。

定义 立方 = 函 x：
  返回 x 相乘 x 相乘 x。
。

打印 "平方(5) = " 平方 5。
打印 "立方(3) = " 立方 3。

# 两数之和函数
定义 a = 10。
定义 b = 20。
定义 和 = a 相加 b。
打印 "10 + 20 = " 和。`,

            condition: `# 条件判断示例
定义 成绩 = 85。

如果 成绩 大于等于 90 那么：
  打印 "优秀"。
否则：
  如果 成绩 大于等于 80 那么：
    打印 "良好"。
  否则：
    如果 成绩 大于等于 60 那么：
      打印 "及格"。
    否则：
      打印 "不及格"。
    。
  。
。`,

            loop: `# 循环遍历示例
定义 水果 = ["苹果", "香蕉", "橘子"]。

打印 "遍历水果列表："。
遍历 水果 于 水果：
  打印 水果。
。

打印 "遍历数字范围："。
遍历 数字 于 范围 1 6：
  打印 数字。
。`,

            fibonacci: `# 斐波那契数列（迭代版本）
定义 a = 0。
定义 b = 1。

打印 "斐波那契数列前10项："。
遍历 i 于 范围 1 11：
  打印 a。
  定义 temp = a。
  定义 a = b。
  定义 b = temp 相加 b。
。`,

            list: `# 列表操作示例
定义 数字 = [1, 2, 3, 4, 5]。

打印 "原始列表：" 数字。
打印 "列表长度：" 长度 数字。

# 计算列表求和
定义 总和 = 0。
遍历 元素 于 数字：
  定义 总和 = 总和 相加 元素。
。

打印 "列表求和：" 总和。`,

            dict: `# 字典操作示例
定义 学生 = {"姓名": "张三", "年龄": 20, "成绩": 85}。

打印 "学生信息：" 学生。
打印 "姓名：" 学生["姓名"]。
打印 "年龄：" 学生["年龄"]。`,

            math: `# 数学运算示例
定义 a = 10。
定义 b = 3。

打印 "a 相加 b = " a 相加 b。
打印 "a 相减 b = " a 相减 b。
打印 "a 相乘 b = " a 相乘 b。
打印 "a 相除 b = " a 相除 b。

定义 x = -5。
打印 "绝对值(-5) = " 绝对值 x。`,

            hanoi: `# 汉诺塔问题（打印移动步骤）
# 将n个盘子从柱子A移动到柱子C，借助柱子B

打印 "汉诺塔3个盘子的移动步骤："。
打印 "第1步：移动盘子1 从A到C"。
打印 "第2步：移动盘子2 从A到B"。
打印 "第3步：移动盘子1 从C到B"。
打印 "第4步：移动盘子3 从A到C"。
打印 "第5步：移动盘子1 从B到A"。
打印 "第6步：移动盘子2 从B到C"。
打印 "第7步：移动盘子1 从A到C"。
打印 "总共需要7步完成。"。
打印 ""。
打印 "汉诺塔递归公式："。
打印 "移动次数 = 2^n - 1"。
打印 "n=3时：2^3 - 1 = 7步"。`,
打印 "第4步：移动盘子3 从A到C"。
打印 "第5步：移动盘子1 从B到A"。
打印 "第6步：移动盘子2 从B到C"。
打印 "第7步：移动盘子1 从A到C"。
打印 "总共需要7步完成。"。`,

            bubble: `# 冒泡排序
打印 "冒泡排序演示"。
打印 "=============="。
打印 ""。
打印 "原始数组：[64, 34, 25, 12, 22, 11, 90]"。
打印 ""。
打印 "排序原理："。
打印 "1. 比较相邻元素"。
打印 "2. 如果前者大于后者，交换位置"。
打印 "3. 重复直到数组有序"。
打印 "4. 时间复杂度：O(n的平方)"。
打印 ""。
打印 "排序过程："。
打印 "第1轮：[34, 25, 12, 22, 11, 64, 90]"。
打印 "第2轮：[25, 12, 22, 11, 34, 64, 90]"。
打印 "第3轮：[12, 22, 11, 25, 34, 64, 90]"。
打印 "第4轮：[12, 11, 22, 25, 34, 64, 90]"。
打印 "第5轮：[11, 12, 22, 25, 34, 64, 90]"。
打印 ""。
打印 "排序后数组：[11, 12, 22, 25, 34, 64, 90]"。`,

            turing: `# 图灵机模拟（二进制加1）
# 模拟图灵机对二进制数加1的操作

打印 "图灵机：二进制加1"。
打印 "=================="。
打印 ""。
打印 "输入纸带：1011 (二进制11)"。
打印 ""。
打印 "执行步骤："。
打印 "1. 移到最右端"。
打印 "2. 当前位是1，写0，左移"。
打印 "3. 当前位是1，写0，左移"。
打印 "4. 当前位是0，写1，停止"。
打印 ""。
打印 "输出纸带：1100 (二进制12)"。
打印 ""。
打印 "验证：11 + 1 = 12 正确"。`,

            prime: `# 埃拉托斯特尼素数筛
# 找出2到30之间的所有素数

打印 "埃拉托斯特尼素数筛"。
打印 "=================="。
打印 ""。
打印 "原理：筛除所有合数，剩下的就是素数"。
打印 ""。

# 手动展示筛法过程
打印 "筛法过程："。
打印 "1. 从2开始，2是素数"。
打印 "2. 筛除2的倍数：4, 6, 8, 10, ..."。
打印 "3. 下一个是3，3是素数"。
打印 "4. 筛除3的倍数：6, 9, 12, 15, ..."。
打印 "5. 下一个是5，5是素数"。
打印 "6. 继续直到√n"。
打印 ""。

打印 "2到30之间的素数："。
打印 2。
打印 3。
打印 5。
打印 7。
打印 11。
打印 13。
打印 17。
打印 19。
打印 23。
打印 29。
打印 ""。
打印 "共找到10个素数。"。`
        };

        const editor = document.getElementById('editor');
        const output = document.getElementById('output');
        const charCount = document.getElementById('charCount');
        const loading = document.getElementById('loading');
        const runStatus = document.getElementById('runStatus');
        const statusInfo = document.getElementById('statusInfo');

        editor.addEventListener('input', () => {
            charCount.textContent = `${editor.value.length} 字符`;
        });

        editor.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                runCode();
            }
        });

        function loadExample(name) {
            console.log('Loading example:', name);
            console.log('Examples object:', examples);
            console.log('Example content:', examples[name]);

            if (!examples[name]) {
                console.error('Example not found:', name);
                output.innerHTML = '<div class="output-error">❌ 示例未找到: ' + name + '</div>';
                return;
            }

            editor.value = examples[name];
            charCount.textContent = `${editor.value.length} 字符`;
            output.innerHTML = '<div class="output-info">▶ 已加载示例，点击「运行代码」执行</div>';

            console.log('Editor value set, length:', editor.value.length);
        }

        async function runCode() {
            const code = editor.value.trim();
            if (!code) {
                output.innerHTML = '<div class="output-error">❌ 请输入代码</div>';
                return;
            }

            loading.classList.add('show');
            runStatus.textContent = '运行中...';
            statusInfo.textContent = '正在执行...';

            const startTime = performance.now();

            try {
                const response = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ code })
                });

                const result = await response.json();
                const endTime = performance.now();
                const duration = (endTime - startTime).toFixed(2);

                if (result.success) {
                    let outputHtml = '';
                    for (const line of result.output) {
                        if (line.startsWith('[ERROR]')) {
                            outputHtml += `<div class="output-error">❌ ${line.substring(7)}</div>`;
                        } else {
                            outputHtml += `<div class="output-success">▶ ${line}</div>`;
                        }
                    }
                    outputHtml += `<div class="output-info" style="margin-top: 15px;">✨ 执行完成，耗时 ${duration}ms</div>`;
                    output.innerHTML = outputHtml;
                } else {
                    output.innerHTML = `<div class="output-error">❌ 执行错误: ${result.error}</div>`;
                }
            } catch (error) {
                output.innerHTML = `<div class="output-error">❌ 网络错误: ${error.message}</div>`;
            }

            loading.classList.remove('show');
            runStatus.textContent = '完成';
            statusInfo.textContent = '就绪';
        }

        function clearOutput() {
            output.innerHTML = '<div class="output-info">▶ 输出已清空</div>';
        }

        function showSyntaxDoc() {
            document.getElementById('syntaxDocModal').style.display = 'flex';
        }

        function hideSyntaxDoc() {
            document.getElementById('syntaxDocModal').style.display = 'none';
        }

        document.getElementById('syntaxDocModal').addEventListener('click', function(e) {
            if (e.target === this) {
                hideSyntaxDoc();
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                hideSyntaxDoc();
            }
        });
    
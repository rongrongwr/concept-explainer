#!/usr/bin/env python3
"""
概念解释 Markdown → PDF 转换脚本 (Chrome Headless版)
用法: python md_to_pdf.py input.md output.pdf [--title "标题"]

依赖: pip install markdown --break-system-packages
      Chrome/Chromium/Edge/Safari 浏览器（系统常见）

支持平台:
- macOS: Chrome, Chromium, Edge, Safari
- Windows: Chrome, Chromium, Edge
- Linux: Chrome, Chromium, Firefox
"""

import sys
import os
import re
import argparse
import subprocess
import tempfile
import platform
import markdown

# ── CSS 样式 ──
CSS_TEMPLATE = """
@media print {
    @page {
        size: A4;
        margin: 25mm 20mm 20mm 20mm;
    }

    body {
        font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.75;
        color: #2c3e50;
        text-align: justify;
    }

    /* 封面 */
    .cover {
        page-break-after: always;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 100vh;
    }
    .cover h1 {
        font-size: 36pt;
        color: #4f46e5;
        margin-bottom: 12mm;
        font-weight: bold;
        letter-spacing: 3pt;
    }
    .cover .subtitle {
        font-size: 14pt;
        color: #95a5a6;
        margin-bottom: 6mm;
    }
    .cover .meta {
        font-size: 11pt;
        color: #95a5a6;
        margin-bottom: 4mm;
    }
    .cover .divider {
        width: 60%;
        margin: 8mm auto;
        border: none;
        border-top: 2pt solid #7c3aed;
    }

    /* 一级标题 */
    h1 {
        font-size: 18pt;
        color: #4f46e5;
        margin-top: 12mm;
        margin-bottom: 6mm;
        padding-bottom: 3mm;
        border-bottom: 2pt solid #4f46e5;
        font-weight: bold;
    }

    /* 二级标题 */
    h2 {
        font-size: 14pt;
        color: #7c3aed;
        margin-top: 10mm;
        margin-bottom: 5mm;
        font-weight: bold;
    }

    /* 三级标题 */
    h3 {
        font-size: 12pt;
        color: #6366f1;
        margin-top: 6mm;
        margin-bottom: 3mm;
        font-weight: bold;
    }

    h4 {
        font-size: 11pt;
        color: #8b5cf6;
        margin-top: 5mm;
        margin-bottom: 2mm;
        font-weight: bold;
    }

    /* 段落 */
    p {
        margin-top: 1.5mm;
        margin-bottom: 1.5mm;
        orphans: 3;
        widows: 3;
    }

    /* 引用块 */
    blockquote {
        margin: 4mm 0;
        padding: 3mm 4mm 3mm 8mm;
        background: #fef9c3;
        border-left: 3pt solid #f59e0b;
        color: #78350f;
        font-size: 10pt;
    }
    blockquote p {
        margin: 1mm 0;
    }
    blockquote strong {
        color: #92400e;
    }

    /* 粗体 */
    strong, b {
        font-weight: bold;
        color: #4f46e5;
    }

    /* 行内代码 */
    code {
        font-family: "Courier New", Monaco, monospace;
        background: #f1f5f9;
        color: #e11d48;
        padding: 0.5mm 1.5mm;
        border-radius: 2pt;
        font-size: 9pt;
    }

    /* 表格 */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 4mm 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }
    thead th {
        background: linear-gradient(to right, #4f46e5, #7c3aed);
        color: white;
        padding: 2.5mm 3mm;
        text-align: left;
        font-weight: bold;
    }
    tbody td {
        padding: 2mm 3mm;
        border-bottom: 0.5pt solid #e2e8f0;
    }
    tbody tr:nth-child(even) {
        background: #f8fafc;
    }

    /* 分隔线 */
    hr {
        border: none;
        border-top: 0.5pt solid #e2e8f0;
        margin: 4mm 0;
    }

    /* 列表 */
    ul, ol {
        margin: 2mm 0;
        padding-left: 8mm;
    }
    li {
        margin-bottom: 1mm;
    }

    /* 链接 */
    a {
        color: #4f46e5;
        text-decoration: none;
    }

    /* 信息来源区块 */
    .sources {
        background: #f8fafc;
        border: 1pt solid #e2e8f0;
        border-radius: 4pt;
        padding: 4mm;
        margin: 4mm 0;
        page-break-inside: avoid;
    }
    .sources h3 {
        margin-top: 0;
        font-size: 10pt;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1pt;
    }
    .sources ul {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    .sources li {
        font-size: 9pt;
        margin-bottom: 1mm;
    }
}

/* 屏幕预览样式 */
@media screen {
    body {
        font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.75;
        color: #2c3e50;
        text-align: justify;
        max-width: 210mm;
        margin: 0 auto;
        padding: 20mm;
    }

    .cover {
        text-align: center;
        padding-top: 20mm;
        margin-bottom: 20mm;
        page-break-after: always;
    }
    .cover h1 {
        font-size: 28pt;
        color: #4f46e5;
        margin-bottom: 8mm;
        font-weight: bold;
        letter-spacing: 2pt;
    }
    .cover .subtitle {
        font-size: 14pt;
        color: #95a5a6;
        margin-bottom: 6mm;
    }
    .cover .meta {
        font-size: 11pt;
        color: #95a5a6;
        margin-bottom: 4mm;
    }
    .cover .divider {
        width: 60%;
        margin: 8mm auto;
        border: none;
        border-top: 2pt solid #7c3aed;
    }

    h1 {
        font-size: 18pt;
        color: #4f46e5;
        margin-top: 12mm;
        margin-bottom: 6mm;
        padding-bottom: 3mm;
        border-bottom: 2pt solid #4f46e5;
        font-weight: bold;
    }

    h2 {
        font-size: 14pt;
        color: #7c3aed;
        margin-top: 10mm;
        margin-bottom: 5mm;
        font-weight: bold;
    }

    h3 {
        font-size: 12pt;
        color: #6366f1;
        margin-top: 6mm;
        margin-bottom: 3mm;
        font-weight: bold;
    }

    h4 {
        font-size: 11pt;
        color: #8b5cf6;
        margin-top: 5mm;
        margin-bottom: 2mm;
        font-weight: bold;
    }

    blockquote {
        margin: 4mm 0;
        padding: 3mm 4mm 3mm 8mm;
        background: #fef9c3;
        border-left: 3pt solid #f59e0b;
        color: #78350f;
    }

    strong, b {
        font-weight: bold;
        color: #4f46e5;
    }

    code {
        font-family: "Courier New", Monaco, monospace;
        background: #f1f5f9;
        color: #e11d48;
        padding: 0.5mm 1.5mm;
        border-radius: 2pt;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 4mm 0;
    }
    thead th {
        background: linear-gradient(to right, #4f46e5, #7c3aed);
        color: white;
        padding: 2.5mm 3mm;
        text-align: left;
        font-weight: bold;
    }
    tbody td {
        padding: 2mm 3mm;
        border-bottom: 0.5pt solid #e2e8f0;
    }
    tbody tr:nth-child(even) {
        background: #f8fafc;
    }

    .sources {
        background: #f8fafc;
        border: 1pt solid #e2e8f0;
        border-radius: 4pt;
        padding: 4mm;
        margin: 4mm 0;
    }
    .sources h3 {
        margin-top: 0;
        font-size: 10pt;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1pt;
    }
    .sources ul {
        list-style: none;
        padding-left: 0;
    }
}
"""


def find_browser():
    """查找系统可用的浏览器"""
    system = platform.system()
    browsers = []

    if system == "Darwin":  # macOS
        browsers = [
            # Chrome
            ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "--headless", "--print-to-pdf={output}", "{html}"],
            # Chromium
            ["/Applications/Chromium.app/Contents/MacOS/Chromium",
             "--headless", "--print-to-pdf={output}", "{html}"],
            # Edge
            ["/Applications/Microsoft Edge.app/Contents/Microsoft Edge",
             "--headless", "--print-to-pdf={output}", "{html}"],
        ]
    elif system == "Windows":
        # Chrome
        chrome_paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                browsers.append([path, "--headless", "--print-to-pdf={output}", "{html}"])

        # Edge
        edge_path = os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe")
        if os.path.exists(edge_path):
            browsers.append([edge_path, "--headless", "--print-to-pdf={output}", "{html}"])
    else:  # Linux
        browsers = [
            ["google-chrome", "--headless", "--print-to-pdf={output}", "{html}"],
            ["chromium", "--headless", "--print-to-pdf={output}", "{html}"],
            ["chromium-browser", "--headless", "--print-to-pdf={output}", "{html}"],
            ["firefox", "--print-to-pdf", "{output}", "{html}"],
        ]

    # 验证浏览器是否存在
    for browser in browsers:
        exe = browser[0]
        if system == "Darwin":
            full_path = exe
        elif system == "Windows":
            full_path = exe
        else:
            # Linux: 检查命令是否存在
            try:
                subprocess.run(["which", exe], capture_output=True, check=True)
                full_path = exe
            except:
                continue

        if system == "Darwin" and not os.path.exists(full_path):
            continue
        if system == "Windows" and not os.path.exists(full_path):
            continue

        return browser

    return None


def md_to_html(md_text, title="概念解释", subtitle="清晰易懂的知识总结",
               meta_line=""):
    """将 Markdown 转为 HTML（无封面）"""

    # 预处理：免责声明替换
    def replace_disclaimer(match):
        content = match.group(1).strip()
        return f'<blockquote class="disclaimer"><p><strong>免责声明</strong>：{content}</p></blockquote>'

    md_text = re.sub(
        r'> \*\*免责声明\*\*[：:](.*?)\n\n*---',
        replace_disclaimer,
        md_text,
        flags=re.DOTALL
    )

    # 用 markdown 库转换正文
    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br'],
        output_format='html5'
    )

    # 后处理：信息来源部分添加样式
    def replace_sources(match):
        content = match.group(1)
        return '<div class="sources">' + content + '</div>'

    html_body = re.sub(
        r'(<h3[^>]*>信息来源</h3>.*?)(?=<h[23]|$)',
        replace_sources,
        html_body,
        flags=re.DOTALL
    )

    # 提取标题用于页面标题
    first_h1_match = re.search(r'<h1>(.*?)</h1>', html_body)
    if first_h1_match:
        extracted_title = first_h1_match.group(1)
        if not title or title == "概念解释":
            title = extracted_title

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{CSS_TEMPLATE}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    return full_html


def main():
    parser = argparse.ArgumentParser(description="概念解释 Markdown → PDF")
    parser.add_argument("input", help="输入的 Markdown 文件路径")
    parser.add_argument("output", help="输出的 PDF 文件路径")
    parser.add_argument("--title", default=None, help="标题")
    parser.add_argument("--open", action="store_true", help="自动打开PDF")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 提取元信息
    meta_line = ""
    for line in md_text.split("\n"):
        stripped = line.strip().lstrip(">").strip()
        if "解释时间" in stripped or "所属领域" in stripped or "概念类型" in stripped:
            meta_line = stripped
            break

    html = md_to_html(md_text, title=args.title or "概念解释", meta_line=meta_line)

    # 保存中间 HTML
    html_path = args.output.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] HTML 已生成: {html_path}")

    # 查找浏览器
    browser = find_browser()
    if not browser:
        print("[警告] 未找到 Chrome/Chromium/Edge 浏览器")
        print("[提示] 请安装 Chrome 或使用浏览器打开 HTML 后手动打印为 PDF")
        print(f"[提示] HTML 文件: {html_path}")
        sys.exit(1)

    # 使用浏览器生成 PDF
    output_abs = os.path.abspath(args.output)
    html_abs = os.path.abspath(html_path)

    # 构建命令
    cmd = []
    for arg in browser:
        if "{output}" in arg:
            cmd.append(arg.replace("{output}", output_abs))
        elif "{html}" in arg:
            cmd.append(arg.replace("{html}", f"file://{html_abs}"))
        else:
            cmd.append(arg)

    print(f"[使用浏览器] {os.path.basename(browser[0])}")

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        size_kb = os.path.getsize(args.output) / 1024
        print(f"[OK] PDF 已生成: {args.output} ({size_kb:.1f} KB)")

        # 自动打开
        if args.open:
            if platform.system() == "Darwin":
                subprocess.run(["open", args.output])
            elif platform.system() == "Windows":
                os.startfile(args.output)
            else:
                subprocess.run(["xdg-open", args.output])

    except subprocess.CalledProcessError as e:
        print(f"[错误] PDF 生成失败: {e}")
        print(f"[提示] 可以手动打开浏览器访问: file://{html_abs}")
        print(f"[提示] 然后使用浏览器的打印功能保存为 PDF")


if __name__ == "__main__":
    main()

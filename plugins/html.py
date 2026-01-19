import os
import webbrowser
import datetime
from cli import command, Color

__author__ = "System"
__category__ = "Reports"
__group__ = "reports"
__desc__ = "HTML Report Management - view and manage generated reports."


def generate_reports_page(reports_dir):
    """Generate an attractive HTML page for reports listing."""
    reports = sorted(
        [f for f in os.listdir(reports_dir) if f.endswith('.html')],
        key=lambda x: os.path.getmtime(os.path.join(reports_dir, x)),
        reverse=True
    )
    
    reports_html = ""
    for idx, report in enumerate(reports, 1):
        filepath = os.path.join(reports_dir, report)
        file_size = os.path.getsize(filepath)
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        size_kb = file_size / 1024
        
        reports_html += f"""
        <div class="report-card">
            <div class="report-header">
                <span class="report-num">#{idx}</span>
                <h3>{report}</h3>
            </div>
            <div class="report-info">
                <span class="info-item">📅 {mod_time.strftime('%d.%m.%Y %H:%M:%S')}</span>
                <span class="info-item">💾 {size_kb:.1f} KB</span>
            </div>
            <a href="{report}" class="btn-open" target="_blank">📊 Open Report</a>
        </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TERMINAL CLI - Reports Hub</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
            color: #e0e0e0;
            font-family: 'Segoe UI', 'Consolas', 'Courier New', monospace;
            line-height: 1.6;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .reports-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .report-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            overflow: hidden;
        }}
        
        .report-card:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(102, 126, 234, 0.5);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }}
        
        .report-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .report-num {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }}
        
        .report-header h3 {{
            font-size: 1.1em;
            word-break: break-word;
            color: #5fbfff;
        }}
        
        .report-info {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #aaa;
        }}
        
        .info-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .btn-open {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
            text-align: center;
            width: 100%;
        }}
        
        .btn-open:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #888;
        }}
        
        .empty-state h2 {{
            font-size: 1.8em;
            margin-bottom: 10px;
            color: #aaa;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 40px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            .reports-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 TERMINAL CLI - Reports Hub</h1>
            <p>Generated Network & System Analysis Reports</p>
        </div>
        
        <div class="reports-grid">
            {reports_html if reports_html else '<div class="empty-state"><h2>📭 No reports yet</h2><p>Generate reports using network analysis commands like <strong>tcp-ip</strong></p></div>'}
        </div>
        
        <div class="footer">
            <p>🔧 TERMINAL CLI v2026 • Report Management System</p>
        </div>
    </div>
</body>
</html>
"""
    return html_content


@command(name="reports", aliases=["html", "show-reports"])
def manage_reports(*args):
    """HTML Report Management - displays list of generated reports."""
    
    reports_dir = os.path.expandvars(r"%userprofile%\.polsoft\psCLI\reports")
    
    if not os.path.exists(reports_dir):
        print(f"{Color.YELLOW}[INFO] No reports directory found. Generate reports with network analysis commands.{Color.RESET}")
        return
    
    try:
        reports = sorted(
            [f for f in os.listdir(reports_dir) if f.endswith('.html')],
            key=lambda x: os.path.getmtime(os.path.join(reports_dir, x)),
            reverse=True
        )
        
        if not reports:
            print(f"{Color.YELLOW}[INFO] No HTML reports found.{Color.RESET}")
            return
        
        print(f"{Color.CYAN}{Color.BOLD}--- AVAILABLE HTML REPORTS ---{Color.RESET}\n")
        
        for idx, report in enumerate(reports, 1):
            filepath = os.path.join(reports_dir, report)
            file_size = os.path.getsize(filepath)
            mod_time = os.path.getmtime(filepath)
            
            size_kb = file_size / 1024
            print(f"{Color.GREEN}[{idx}]{Color.RESET} {report:<40} ({size_kb:.1f} KB)")
        
        print(f"\n{Color.CYAN}Type 'show-report <number>' to open a report.{Color.RESET}")
        print(f"{Color.CYAN}Example: show-report 1{Color.RESET}\n")
        
    except Exception as e:
        print(f"{Color.RED}[ERROR] Could not list reports: {e}{Color.RESET}")


@command(name="show-report", aliases=["open-report", "view-report"])
def show_report(*args):
    """Open HTML report in default browser."""
    
    if not args:
        print(f"{Color.RED}[ERROR] Usage: show-report <report_name or number>{Color.RESET}")
        return
    
    reports_dir = os.path.expandvars(r"%userprofile%\.polsoft\psCLI\reports")
    
    if not os.path.exists(reports_dir):
        print(f"{Color.RED}[ERROR] Reports directory not found.{Color.RESET}")
        return
    
    try:
        reports = sorted(
            [f for f in os.listdir(reports_dir) if f.endswith('.html')],
            key=lambda x: os.path.getmtime(os.path.join(reports_dir, x)),
            reverse=True
        )
        
        if not reports:
            print(f"{Color.RED}[ERROR] No reports available.{Color.RESET}")
            return
        
        # Try to parse as number (index)
        try:
            idx = int(args[0]) - 1
            if 0 <= idx < len(reports):
                report_name = reports[idx]
            else:
                print(f"{Color.RED}[ERROR] Invalid report number.{Color.RESET}")
                return
        except ValueError:
            # Try to find by name
            report_name = args[0]
            if not report_name.endswith('.html'):
                report_name += '.html'
            
            if report_name not in reports:
                print(f"{Color.RED}[ERROR] Report not found: {report_name}{Color.RESET}")
                return
        
        filepath = os.path.join(reports_dir, report_name)
        webbrowser.open(f"file:///{filepath.replace(chr(92), '/')}")
        print(f"{Color.GREEN}[OK] Opening {report_name} in default browser...{Color.RESET}")
        
    except Exception as e:
        print(f"{Color.RED}[ERROR] Could not open report: {e}{Color.RESET}")


@command(name="reports-hub", aliases=["hub", "dashboard"])
def reports_hub(*args):
    """Open Reports Hub - interactive dashboard for all reports."""
    
    reports_dir = os.path.expandvars(r"%userprofile%\.polsoft\psCLI\reports")
    
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir, exist_ok=True)
    
    try:
        hub_path = os.path.join(reports_dir, "index.html")
        html_content = generate_reports_page(reports_dir)
        
        with open(hub_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        webbrowser.open(f"file:///{hub_path.replace(chr(92), '/')}")
        print(f"{Color.GREEN}[OK] Opening Reports Hub in default browser...{Color.RESET}")
        
    except Exception as e:
        print(f"{Color.RED}[ERROR] Could not open Reports Hub: {e}{Color.RESET}")

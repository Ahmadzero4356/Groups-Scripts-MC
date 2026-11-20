#!/usr/bin/env python3
"""أدوات بسيطة لمستودع سكربتات Skript.

الاستخدام (من جذر المستودع):
    python3 tools/repo_tool.py check            # فحص ملفات .sk الفعّالة
    python3 tools/repo_tool.py release          # بناء ملفات ZIP في releases/
    python3 tools/repo_tool.py list             # عرض ملفات المستودع

الفحص لا يعدّل أي ملف. يُرجع الكود 1 إذا وُجدت أخطاء (وليس تحذيرات فقط).
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUPS = ["Core boot", "claim (GriefPrevention)", "item admin"]
SKIP_DIRS = {"archive", "releases", "tools", ".git"}


def active_files():
    """ملفات .sk الفعّالة فقط (تستثني الأرشيف)."""
    for path in sorted(ROOT.rglob("*.sk")):
        if not SKIP_DIRS & set(path.relative_to(ROOT).parts):
            yield path


def split_code_comment(line):
    """يفصل الكود عن التعليق (# خارج النصوص)."""
    in_str = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_str = not in_str
        elif ch == "#" and not in_str:
            return line[:i], line[i:]
    return line, ""


def check_file(path):
    problems = []  # (line_no, severity, message)
    lines = path.read_text(encoding="utf-8").splitlines()
    text_lines = []
    in_options = False
    params = set()
    func_re = re.compile(r"^function\s+\w+\((.*?)\)")

    for n, raw in enumerate(lines, 1):
        code, _comment = split_code_comment(raw)
        stripped = code.strip()
        indent = len(code) - len(code.lstrip(" \t"))

        if "\t" in code[:indent]:
            problems.append((n, "error", "tab used for indentation"))
        elif stripped and indent % 4:
            problems.append((n, "warning", f"indent {indent} is not a multiple of 4"))

        if stripped and code.count('"') % 2:
            problems.append((n, "error", "unbalanced double quote (stray or missing \")"))
        if stripped and code.count("{") != code.count("}"):
            problems.append((n, "error", "unbalanced { } braces"))

        if not raw.startswith((" ", "\t")) and stripped:
            in_options = stripped == "options:"
        if in_options and indent > 0 and ":" in code and _comment:
            # قيمة في options مع تعليق # في نفس السطر
            problems.append((n, "warning", "inline # comment after an options value (move it to its own line)"))

        m = func_re.match(raw)
        if m:
            params = {p.split(":")[0].strip() for p in m.group(1).split(",") if p.strip()}

        # معاملات الدالة محلية وتُقرأ بـ {_name}؛ استخدام {name} بدون _ خطأ شائع
        for p in params:
            if re.search(r"(?<![\w_])\{" + re.escape(p) + r"(\}|::)", code):
                problems.append((n, "error", f"function parameter '{p}' read as global {{{p}}} (use {{_{p}}})"))

        text_lines.append((n, indent, stripped, code))

    # كل سطر ينتهي بـ ":" يجب أن يتبعه سطر مُزاح للداخل
    code_lines = [t for t in text_lines if t[2] and not t[2].startswith("#")]
    for idx, (n, indent, stripped, _code) in enumerate(code_lines):
        if stripped.endswith(":"):
            if idx + 1 >= len(code_lines) or code_lines[idx + 1][1] <= indent:
                problems.append((n, "error", "block header ':' has no indented body"))

    return problems


def cmd_check():
    total_err = total_warn = 0
    files = list(active_files())
    for path in files:
        rel = path.relative_to(ROOT)
        for n, sev, msg in check_file(path):
            print(f"{rel}:{n}: {sev}: {msg}")
            total_err += sev == "error"
            total_warn += sev == "warning"
    print(f"\nchecked {len(files)} file(s): {total_err} error(s), {total_warn} warning(s)")
    return 1 if total_err else 0


def cmd_release():
    out = ROOT / "releases"
    out.mkdir(exist_ok=True)
    for group in GROUPS:
        src = ROOT / group
        if not src.is_dir():
            print(f"skip (missing): {group}")
            continue
        zip_name = out / f"{group.replace(' ', '-').replace('(', '').replace(')', '')}.zip"
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(src.rglob("*")):
                if f.is_file() and f.suffix == ".sk":
                    zf.write(f, f.relative_to(ROOT))
        print(f"built {zip_name.relative_to(ROOT)}")
    return 0


def cmd_list():
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts):
        print(path.relative_to(ROOT))
    return 0


def main(argv):
    commands = {"check": cmd_check, "release": cmd_release, "list": cmd_list}
    if len(argv) != 2 or argv[1] not in commands:
        print(__doc__)
        return 2
    return commands[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""Extract NUnit/xUnit tests from C# files into JSON records."""
import json, re, sys, os

ATTR_START = re.compile(r'^\s*\[')
TEST_ATTR = re.compile(r'\[\s*(Test|Fact|Theory|TestCase|TestCaseSource|InlineData|MemberData'
                       r'|RetryTest|CiTest|TestDescription|Ignore|Explicit|Retry)\b')
IS_TEST_MARK = re.compile(r'\[\s*(Test|Fact|Theory|RetryTest|CiTest)\s*[\],(\]]')
CASE_ATTR = re.compile(r'^\s*\[\s*(TestCase|InlineData)\s*\((.*)\)\s*\]\s*(?://.*)?$', re.S)
CASE_SRC = re.compile(r'^\s*\[\s*(TestCaseSource|MemberData)\s*\(')
DESC = re.compile(r'(?:Test)?Description\s*(?:=\s*|\(\s*)"((?:[^"\\]|\\.)*)"')
METHOD = re.compile(r'^\s*(?:public|private|protected|internal)\s+(?:static\s+)?(?:async\s+)?[\w<>,\[\]\?\. ]+?\s+(\w+)\s*\(')
CLASS = re.compile(r'^\s*(?:public|internal|abstract|sealed|partial|\s)*class\s+(\w+)')
CATEGORY = re.compile(r'\[\s*Category\s*\(\s*"([^"]+)"')
IGNORED = re.compile(r'\[\s*(Ignore|Explicit)\s*[\(\]]')
RETRY = re.compile(r'\[\s*(RetryTest|Retry)\s*[\(\]]')
CITEST = re.compile(r'\[\s*CiTest\s*[\(\]]')
VALUES = re.compile(r'\[\s*(Values|BoolValues)\b')

def split_args(s):
    out, depth, cur, instr, esc = [], 0, '', None, False
    for ch in s:
        if esc: cur += ch; esc = False; continue
        if instr:
            cur += ch
            if ch == '\\': esc = True
            elif ch == instr: instr = None
            continue
        if ch in '"\'': instr = ch; cur += ch; continue
        if ch in '([{': depth += 1
        elif ch in ')]}': depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    return out

def body_of(lines, start):
    """Return body text starting at method decl line index, matching braces."""
    depth, started, buf = 0, False, []
    for i in range(start, min(start + 400, len(lines))):
        ln = lines[i]
        buf.append(ln)
        for ch in ln:
            if ch == '{': depth += 1; started = True
            elif ch == '}':
                depth -= 1
                if started and depth == 0:
                    return '\n'.join(buf), i
    return '\n'.join(buf), min(start + 400, len(lines)) - 1

def extract(path, repo_rel):
    src = open(path, encoding='utf-8', errors='replace').read()
    lines = src.split('\n')
    recs, cur_class, pending = [], None, []
    i = 0
    while i < len(lines):
        ln = lines[i]
        cm = CLASS.match(ln)
        if cm: cur_class = cm.group(1)
        if ATTR_START.match(ln) and TEST_ATTR.search(ln):
            pending.append((i, ln))
            i += 1
            continue
        if ATTR_START.match(ln) and not TEST_ATTR.search(ln):
            if CATEGORY.search(ln) or DESC.search(ln): pending.append((i, ln))
            i += 1
            continue
        mm = METHOD.match(ln)
        if mm and pending:
            attrs = [a for _, a in pending]
            attrtext = ' '.join(attrs)
            has_case = any(CASE_ATTR.match(a) or CASE_SRC.match(a) for a in attrs)
            if IS_TEST_MARK.search(attrtext) or has_case:
                name = mm.group(1)
                decl_line = i + 1
                body, endi = body_of(lines, i)
                d = DESC.search(attrtext)
                cats = CATEGORY.findall(attrtext)
                cases = []
                for a in attrs:
                    cmt = CASE_ATTR.match(a)
                    if cmt: cases.append(split_args(cmt.group(2)))
                    elif CASE_SRC.match(a): cases.append(['<data-driven>'])
                sig_start = ln
                combinatorial = bool(VALUES.search(ln)) or bool(VALUES.search(body[:600]))
                recs.append(dict(file=repo_rel, cls=cur_class, name=name, line=decl_line,
                                 desc=d.group(1) if d else None, cases=cases, body=body,
                                 categories=cats, attrs=attrs,
                                 ignored=bool(IGNORED.search(attrtext)),
                                 retry=bool(RETRY.search(attrtext)),
                                 citest=bool(CITEST.search(attrtext)),
                                 combinatorial=combinatorial))
            pending = []
            i += 1
            continue
        if ln.strip() and not ATTR_START.match(ln):
            if not ln.strip().startswith('//') and not ln.strip().startswith('*') and not ln.strip().startswith('/*'):
                pending = []
        i += 1
    return recs

if __name__ == '__main__':
    root, prefix = sys.argv[1], sys.argv[2]
    pats = sys.argv[3:] if len(sys.argv) > 3 else []
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('.git', 'obj', 'bin', 'node_modules')]
        for f in fn:
            if not f.endswith('.cs'): continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root)
            repo_rel = os.path.join(prefix, rel) if prefix else rel
            if pats and not any(p in repo_rel for p in pats): continue
            try: out.extend(extract(full, repo_rel))
            except Exception as e: print(f"ERR {repo_rel}: {e}", file=sys.stderr)
    json.dump(out, sys.stdout)

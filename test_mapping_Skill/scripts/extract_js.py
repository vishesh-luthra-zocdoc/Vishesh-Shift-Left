#!/usr/bin/env python3
"""Extract Jest/Playwright tests (describe/it/test blocks) from TS/JS files."""
import json, re, sys, os

BLOCK = re.compile(r'^(\s*)(describe|context|it|test)((?:\.(?:each|only|skip|todo|concurrent|describe|fixme|serial|parallel|failing|beforeEach|afterEach|step|use))*)\s*(?=[<(`])')
NAME_AFTER = re.compile(r'^\s*[\'"`]((?:[^\'"`\\]|\\.)*)[\'"`]')

def find_name(text, idx):
    """From the '(' position, get the first string-literal argument (handles template literals)."""
    j = idx
    n = len(text)
    while j < n and text[j] in ' \t\n(': j += 1
    if j >= n or text[j] not in '\'"`': return None, j
    q = text[j]; j += 1; buf = []
    while j < n:
        c = text[j]
        if c == '\\': buf.append(text[j:j+2]); j += 2; continue
        if c == q: return ''.join(buf), j
        buf.append(c); j += 1
    return ''.join(buf), j

def match_close(text, i):
    """i points at an opening bracket; return index just past its match."""
    pairs = {'(': ')', '[': ']', '{': '}', '`': '`'}
    if text[i] not in pairs: return i
    if text[i] == '`':
        j = i + 1
        while j < len(text):
            if text[j] == '\\': j += 2; continue
            if text[j] == '`': return j + 1
            j += 1
        return j
    depth, j, instr, esc = 0, i, None, False
    while j < len(text):
        ch = text[j]
        if esc: esc = False; j += 1; continue
        if instr:
            if ch == '\\': esc = True
            elif ch == instr: instr = None
            j += 1; continue
        if ch in '"\'`': instr = ch; j += 1; continue
        if ch in '([{': depth += 1
        elif ch in ')]}':
            depth -= 1
            if depth == 0: return j + 1
        j += 1
    return j


def skip_generics(text, j):
    """If a balanced <...> starts at j, skip past it."""
    n = len(text)
    while j < n and text[j] in ' \t\n': j += 1
    if j >= n or text[j] != '<': return j
    depth = 0
    while j < n:
        ch = text[j]
        if ch == '<': depth += 1
        elif ch == '>':
            depth -= 1
            if depth == 0: return j + 1
        elif ch in '()`;{}' and depth == 0: return j
        j += 1
    return j


def find_each_name(text, paren_idx):
    """it.each([...])('name', fn) — skip the cases arg, then read the title string."""
    n = len(text)
    j = paren_idx
    while j < n and text[j] in ' \t\n': j += 1
    if j < n and text[j] == '(':
        j = match_close(text, j)          # past (cases)
    elif j < n and text[j] == '`':
        j = match_close(text, j)          # past `table`
    while j < n and text[j] in ' \t\n': j += 1
    if j < n and text[j] == '(':
        nm, end = find_name(text, j)
        if nm: return nm, end
    # Fallback: bracket scanning can be defeated by regex literals containing
    # quotes (e.g. /you've/). Find the first `)(` followed by a string literal.
    m = re.compile(r"\)\s*\(\s*['\"`]").search(text, paren_idx)
    if m:
        return find_name(text, m.end() - 1)
    return None, j


def block_body(lines, start_i, indent, col=0):
    """Collect lines until the block's brackets close. `col` skips chars on the first line."""
    depth, started, buf = 0, False, []
    for i in range(start_i, min(start_i + 250, len(lines))):
        ln = lines[i]; buf.append(ln)
        if i == start_i and col: ln = ln[col:]
        instr = None; esc = False
        for ch in ln:
            if esc: esc = False; continue
            if instr:
                if ch == '\\': esc = True
                elif ch == instr: instr = None
                continue
            if ch in '"\'`': instr = ch; continue
            if ch in '({[': depth += 1; started = True
            elif ch in ')}]':
                depth -= 1
                if started and depth <= 0:
                    return '\n'.join(buf), i
    return '\n'.join(buf), min(start_i + 250, len(lines)) - 1

def each_cases(text, paren_idx):
    """Return a list of human labels for it.each cases, or None."""
    n = len(text)
    j = paren_idx
    while j < n and text[j] in ' \t\n': j += 1
    if j >= n: return None
    if text[j] == '`':                      # tagged-template table
        end = match_close(text, j)
        rows = [r.strip() for r in text[j+1:end-1].split('\n') if r.strip()]
        rows = [r for r in rows if not set(r) <= set('|- ')]
        return [re.sub(r'\s*\|\s*', ' | ', r).strip(' |') for r in rows[1:]] or None
    if text[j] != '(': return None
    inner_start = j + 1
    inner_end = match_close(text, j) - 1
    seg = text[inner_start:inner_end].strip()
    seg = re.sub(r'\s+as\s+const\s*$', '', seg).strip()
    if not seg.startswith('['): return None
    arr_end = match_close(seg, 0)
    body = seg[1:arr_end - 1]
    # split top-level commas
    items, depth, cur, instr, esc = [], 0, '', None, False
    for ch in body:
        if esc: cur += ch; esc = False; continue
        if instr:
            cur += ch
            if ch == '\\': esc = True
            elif ch == instr: instr = None
            continue
        if ch in '"\'`': instr = ch; cur += ch; continue
        if ch in '([{': depth += 1
        elif ch in ')]}': depth -= 1
        if ch == ',' and depth == 0:
            items.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): items.append(cur.strip())
    labels = []
    for it in items:
        t = re.sub(r'\s+', ' ', it).strip()
        if t.startswith('[') or t.startswith('{'):
            t = t[1:-1].strip() if len(t) > 1 else t
        t = re.sub(r'^\s*', '', t)
        labels.append(t[:70])
    return labels or None


def subst_name(name, label):
    """Fill jest printf/$named placeholders in a title with the case label."""
    if not name: return name
    parts = [p.strip().strip('"\'`') for p in re.split(r',(?![^\[\]{}()]*[\]}\)])', label)]
    out = name
    if re.search(r'%[sdifjoOp#]', out):
        for p in parts:
            out = re.sub(r'%[sdifjoOp#]', lambda _m, _v=p: _v, out, count=1)
    if '$' in out:
        for m in set(re.findall(r'\$(\w+)', out)):
            v = None
            fm = re.search(r'\b' + re.escape(m) + r'\s*:\s*([^,}]+)', label)
            if fm: v = fm.group(1).strip().strip('"\'`')
            if v: out = out.replace('$' + m, v)
    return out


def extract(path, repo_rel):
    src = open(path, encoding='utf-8', errors='replace').read()
    lines = src.split('\n')
    recs, stack = [], []
    line_start, acc = [], 0
    for l in lines:
        line_start.append(acc); acc += len(l) + 1
    for i, ln in enumerate(lines):
        m = BLOCK.match(ln)
        if not m: continue
        indent, kind, mods = m.group(1), m.group(2), m.group(3) or ''
        pos = m.end()
        abs_pos = line_start[i] + pos
        abs_pos = skip_generics(src, abs_pos)
        if '.each' in mods:
            name, _ = find_each_name(src, abs_pos)
        else:
            name, _ = find_name(src, abs_pos)
        # test.step/hooks are not tests; test.describe is a suite, not a test
        if any(h in mods for h in ('.step', '.beforeEach', '.afterEach', '.beforeAll',
                                   '.afterAll', '.use', '.setTimeout', '.slow')):
            continue
        stack = [s for s in stack if len(s[0]) < len(indent)]
        if kind in ('describe', 'context') or '.describe' in mods:
            stack.append((indent, name or '(unnamed)'))
            continue
        body_start, body_col = i, 0
        if '.each' in mods:
            # skip the cases argument so the body scan starts at the callback call
            k = abs_pos
            while k < len(src) and src[k] in ' \t\n': k += 1
            if k < len(src) and src[k] in '(`':
                k = match_close(src, k)
                while k < len(src) and src[k] in ' \t\n': k += 1
                if k < len(src) and src[k] == '(':
                    body_start = src.count('\n', 0, k)
                    body_col = k - line_start[body_start]
        body, endi = block_body(lines, body_start, indent, body_col)
        cases = each_cases(src, abs_pos) if '.each' in mods else None
        recs.append(dict(file=repo_rel, name=name or '(unnamed)', line=i + 1,
                         suites=[s[1] for s in stack], mods=mods, body=body,
                         each=len(cases) if cases else None, case_labels=cases,
                         case_names=[subst_name(name, c) for c in cases] if cases else None,
                         skipped=('.skip' in mods or '.todo' in mods),
                         only=('.only' in mods)))
    return recs

if __name__ == '__main__':
    root, prefix = sys.argv[1], sys.argv[2]
    files = [l.strip() for l in sys.stdin if l.strip()]
    out = []
    for rel in files:
        full = os.path.join(root, rel)
        if not os.path.isfile(full): print(f"MISSING {rel}", file=sys.stderr); continue
        repo_rel = os.path.join(prefix, rel) if prefix else rel
        try: out.extend(extract(full, repo_rel))
        except Exception as e: print(f"ERR {rel}: {e}", file=sys.stderr)
    json.dump(out, sys.stdout)

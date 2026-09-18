#!/usr/bin/env python3
"""Render extracted test records into a test-mapping markdown doc per format-spec.md."""
import json, re, sys, os, datetime

def esc(s):
    if s is None: return ''
    s = re.sub(r'\s+', ' ', str(s)).strip()
    return s.replace('\\', '\\\\').replace('|', '\\|')

def humanize(name):
    """MethodName_Case_Expected -> readable phrase."""
    n = name
    n = re.sub(r'^(should|test)_?', '', n, flags=re.I)
    parts = [p for p in n.split('_') if p]
    if len(parts) > 1:
        out = []
        for p in parts:
            p = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', p)
            out.append(p)
        return ' — '.join(out)
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', n)

# ---------- signal extraction from a test body ----------
ASSERT_PATTERNS = [
    (re.compile(r'\.Should\(\)\.([A-Za-z]+)'), 'FluentAssertions {0}'),
    (re.compile(r'Assert\.That\('), 'Assert.That'),
    (re.compile(r'Assert\.(AreEqual|IsTrue|IsFalse|IsNull|IsNotNull|Throws\w*|AreNotEqual|Greater|Less)'), 'Assert.{0}'),
    (re.compile(r'expect\(.{0,600}?\)\s*\.\s*(?:not\s*\.\s*)?'
                r'(?:resolves\s*\.\s*|rejects\s*\.\s*)?(?:not\s*\.\s*)?(to[A-Za-z]+)', re.S),
     'expect(...).{0}'),
    (re.compile(r'(expectV2MetricWasSentWith|expectMetricWasSentWith|expect\w*WasSent\w*)\('),
     '{0}(...)'),
    (re.compile(r'\.(toHaveBeenCalled\w*|toMatchSnapshot|toThrow\w*)\('), 'assert .{0}'),
    (re.compile(r'\bawait expect\('), 'await expect(...)'),
    (re.compile(r'Verify\('), 'Moq Verify'),
]
HTTP = re.compile(r'\b(GetAsync|PostAsync|PutAsync|DeleteAsync|PatchAsync|SendAsync)\b')
ROUTE = re.compile(r'["\'`]\$?(/[A-Za-z0-9\-]+/v\d[A-Za-z0-9/_\-\{\}\.\$:]*'
                   r'|/(?:v\d|api)[A-Za-z0-9/_\-\{\}\.\$:]*)["\'`]')
STATUS = re.compile(r'HttpStatusCode\.(\w+)|status\(\)\s*\)\.toBe\((\d{3})\)|\.status\s*===?\s*(\d{3})')
PW_ACTIONS = re.compile(r'\.(goto|click|fill|press|check|uncheck|selectOption|hover|type|setInputFiles|waitForURL|waitForResponse)\(')
PW_LOCATOR = re.compile(r'(?:getByTestId|getByRole|getByText|getByLabel|locator)\(\s*[\'"`]([^\'"`]{1,48})')
RTL_ACTIONS = re.compile(r'(?:userEvent|fireEvent)\.(\w+)\(')
RENDER = re.compile(r'\b(render|renderHook|mount)\s*\(')
MOCKS = re.compile(r'(jest\.mock|page\.route|route\.fulfill|new Mock<|Substitute\.For|MockRepository|installStripeJsFake|msw|nock)')
DB = re.compile(r'(DbContext|UseInMemoryDatabase|BeginTransaction|SaveChanges|Database\.)')
CS_ACT = re.compile(r'\b(?:var|await)\s+\w+\s*=\s*(?:await\s+)?_?(?:sut|service|handler|target|subject|controller|client)\.(\w+)')

def sniff(body, kind):
    """Return (steps, summary_bits, scope_bits) derived from the body."""
    b = body or ''
    steps, notes = [], []

    if kind in ('unit', 'api', 'integration', 'cron') or (kind in ('selenium', 'e2e') and 'Assert' in b):
        # Arrange
        if DB.search(b): notes.append('real DbContext / in-memory DB')
        mo = re.findall(r'new Mock<I?(\w+)>', b)
        if mo:
            uniq = sorted(set(mo))[:3]
            steps.append('Arrange mocks (' + ', '.join(uniq) + ')')
        elif re.search(r'\b(Arrange|Given)\b', b):
            steps.append('Arrange fixture')
        # Act
        acts = CS_ACT.findall(b)
        calls = []
        for m in HTTP.finditer(b):
            verb = m.group(1).replace('Async', '').upper()
            rm = ROUTE.search(b, m.end(), m.end() + 400)
            calls.append((verb, rm.group(1) if rm else 'endpoint'))
        if calls:
            seen = []
            for verb, route in calls:
                sig = f'{verb} {route}'
                if sig not in seen: seen.append(sig)
            steps.append(' -> '.join(seen[:3]))
        elif acts:
            steps.append('Call ' + acts[0] + '()')
        # Assert
        codes = []
        for m in STATUS.finditer(b):
            c = next((g for g in m.groups() if g), None)
            if c and c not in codes: codes.append(c)
        if codes:
            steps.append('Assert status ' + '/'.join(codes[:3]))
        for pat, tmpl in ASSERT_PATTERNS:
            m = pat.search(b)
            if m:
                g = m.group(1) if m.groups() and m.group(1) else ''
                steps.append('Assert ' + (tmpl.format(g) if '{0}' in tmpl else tmpl))
                break
        if re.search(r'Throws|ThrowAsync|Assert\.Throws', b): notes.append('asserts the throw path')
        if MOCKS.search(b): notes.append('collaborators mocked')

    else:  # component / e2e / selenium
        rh = re.search(r'\brenderHook\s*\(', b)
        if rh: steps.append('Render hook (renderHook)')
        elif RENDER.search(b): steps.append('Render component')
        if re.search(r'\bact\s*\(', b): steps.append('act()')
        if re.search(r'page\.goto\(', b):
            m = re.search(r'goto\(\s*[\'"`]([^\'"`]{1,60})', b)
            steps.append(f"Navigate {m.group(1)}" if m else 'Navigate to page')
        elif re.search(r'visitBillingSettings|visit\w*Page|loadPage', b):
            steps.append('Load billing page (stubbed API)')
        acts = PW_ACTIONS.findall(b) or RTL_ACTIONS.findall(b)
        if acts:
            seen, ordered = set(), []
            for a in acts:
                if a not in seen and a != 'goto':
                    seen.add(a); ordered.append(a)
            if ordered: steps.append('Interact: ' + ', '.join(ordered[:4]))
        loc = PW_LOCATOR.findall(b)
        if loc: notes.append('targets ' + ', '.join(sorted(set(loc))[:2]))
        for pat, tmpl in ASSERT_PATTERNS:
            m = pat.search(b)
            if m:
                g = m.group(1) if m.groups() and m.group(1) else ''
                steps.append('Assert ' + (tmpl.format(g) if '{0}' in tmpl else tmpl))
                break
        if MOCKS.search(b): notes.append('backend/Stripe stubbed')
        if re.search(r'if\s*\(.*(?:mock|find)\(.*\)\s*\)\s*\{[^}]*expect', b, re.S):
            notes.append('CONDITIONAL assertion — can pass as a no-op')

    if not steps: steps = ['Execute test body']
    n_assert = len(re.findall(r'(?:expect\(|Assert\.|\.Should\(\)|Verify\()', b))
    return steps, notes, n_assert

def build_rows(recs, kind, owner, repo, sha, start_num=1):
    """Group records by file; return list of (file, rows)."""
    byfile = {}
    for r in recs: byfile.setdefault(r['file'], []).append(r)
    n = start_num
    out = []
    for f in sorted(byfile):
        rows = []
        for r in sorted(byfile[f], key=lambda x: x['line']):
            steps, notes, n_assert = sniff(r.get('body', ''), kind)
            link = f"[L{r['line']}](https://github.com/{owner}/{repo}/blob/{sha}/{r['file']}#L{r['line']})"
            suites = r.get('suites') or ([r['cls']] if r.get('cls') else [])
            ctx = ' > '.join([s for s in suites if s]) if suites else ''
            desc = r.get('desc')
            base_name = r['name']

            # case expansion
            cases = r.get('cases') or []
            variants, variant_names = [], []
            if cases:                                    # C# [TestCase]/[InlineData]
                for c in cases:
                    label = ', '.join(x.strip().strip('"') for x in c)[:60] if isinstance(c, list) else str(c)[:60]
                    variants.append(label or 'case')
            elif r.get('case_labels'):                   # JS it.each — real values
                variants = [c[:60] for c in r['case_labels']]
                variant_names = r.get('case_names') or []

            def compose(nm):
                w = desc or humanize(nm)
                return (f'{ctx}: {w}' if ctx else w), w
            what_full, what = compose(base_name)

            flags = []
            if r.get('ignored'): flags.append('**[Ignore]**')
            if r.get('skipped'): flags.append('**skipped**')
            if r.get('only'): flags.append('**.only**')
            if r.get('retry'): flags.append('retry-on-fail')
            if r.get('citest'): flags.append('CI-gated')
            if r.get('combinatorial'): flags.append('combinatorial [Values]')

            def mk_summary(w):
                t = desc or w
                t = t[0].upper() + t[1:] if t else t
                if not t.endswith('.'): t += '.'
                if n_assert: t += f' {n_assert} assertion{"s" if n_assert != 1 else ""}.'
                return t
            summary = mk_summary(what)

            unit = (suites[0] if suites else None) or os.path.basename(r['file']).split('-tests')[0].split('.test')[0]
            level = {'unit': 'L1 unit', 'component': 'L2 component', 'integration': 'L3 integration',
                     'api': 'L4 api', 'cron': 'L1 unit (cron handler)',
                     'playwright': 'L5 e2e', 'cypress': 'L5 e2e',
                     'selenium': 'L5 e2e', 'e2e': 'L5 e2e'}.get(kind, kind)
            if kind == 'unit' and re.search(r'\b(render|renderHook|mount)\s*\(', r.get('body') or ''):
                level = 'L2 component'
            if r.get('is_cron') and '(cron handler)' not in level:
                level += ' (cron handler)'
            scope = f'{level}. In scope: `{unit}`.'
            oos = []
            if MOCKS.search(r.get('body') or ''): oos.append('mocked collaborators not exercised')
            if kind in ('playwright', 'cypress') or r.get('driver') == 'playwright':
                oos.append('no real backend or Stripe')
            if kind == 'selenium' or r.get('driver') == 'selenium':
                oos.append('drives a real browser; slow and order-sensitive')
            if oos: scope += ' Out of scope: ' + '; '.join(oos) + '.'
            extra = list(notes)
            if flags: extra = flags + extra
            if extra: scope += ' ' + '; '.join(extra) + '.'

            if variants:
                for vi, v in enumerate(variants):
                    disp = base_name
                    if variant_names and vi < len(variant_names) and variant_names[vi]:
                        disp = variant_names[vi]
                    wf, w = compose(disp)
                    if cases:                      # C#: show the case tuple explicitly
                        wf = f'{wf} — case: {v}'
                    rows.append((n, f'{disp} ({v})', wf, ' -> '.join(steps),
                                 mk_summary(w), scope, link))
                    n += 1
            else:
                rows.append((n, base_name, what_full, ' -> '.join(steps), summary, scope, link))
                n += 1
        out.append((f, rows))
    return out, n

HEADER = """# {title}

<!-- test-mapping-meta
repo: {owner}/{repo}
branch: {branch}
commit: {sha}
generated: {date}
test-type: {kind}
-->
> Source: {owner}/{repo} @ `{short}` · branch `{branch}` · generated {date}
"""

def render(recs, *, title, owner, repo, branch, sha, kind, date, intro='', start_num=1):
    files, next_n = build_rows(recs, kind, owner, repo, sha, start_num)
    parts = [HEADER.format(title=title, owner=owner, repo=repo, branch=branch,
                           sha=sha, short=sha[:10], date=date, kind=kind)]
    if intro: parts.append('\n' + intro.rstrip() + '\n')
    total = sum(len(rows) for _, rows in files)
    parts.append(f'\n**{len(files)} test files · {total} mapped rows**\n')
    for i, (f, rows) in enumerate(files):
        parts.append(f'\n---\n\n## {f}\n')
        parts.append('| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |')
        parts.append('|---|-----------|---------------|-------|---------|-------|-------------|')
        for (n, name, what, steps, summary, scope, link) in rows:
            parts.append(f'| {n} | `{esc(name)}` | {esc(what)} | {esc(steps)} | {esc(summary)} | {esc(scope)} | {link} |')
    return '\n'.join(parts) + '\n', next_n, total, len(files)

if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1]))
    recs = json.load(open(cfg['records']))
    if cfg.get('filter_prefixes'):
        recs = [r for r in recs if any(r['file'].startswith(p) for p in cfg['filter_prefixes'])]
    md, nxt, total, nfiles = render(recs, title=cfg['title'], owner=cfg['owner'], repo=cfg['repo'],
        branch=cfg['branch'], sha=cfg['sha'], kind=cfg['kind'],
        date=cfg.get('date') or datetime.date.today().isoformat(),
        intro=cfg.get('intro',''), start_num=cfg.get('start_num',1))
    open(cfg['out'],'w').write(md)
    print(f"{cfg['out']}: {nfiles} files, {total} rows")

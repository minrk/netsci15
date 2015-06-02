import io
import json
from subprocess import check_output, Popen, PIPE
from IPython import nbformat
from IPython.display import display, HTML

def add_style():
    style = check_output('pygmentize -S friendly -f html -a .pygments'.split()).decode('utf8')
    display(HTML('<style type="text/css">%s</style>' % style))
    
add_style()

def show_ipynb(filename, limit=10, tail=False):
    with io.open(filename, 'rb') as f:
        data = f.read()
    lines = data.split(b'\n')
    if tail:
        lines = lines[-limit:]
    else:
        lines = lines[:limit]
    p = Popen('pygmentize -l json -f html -O cssclass=pygments'.split(), stdin=PIPE, stdout=PIPE)
    out, _ = p.communicate(b'\n'.join(lines))
    display(HTML(out.decode('utf8')))

def summarize_json(obj):
    if isinstance(obj, list):
        if obj and isinstance(obj[0], str):
            return '[ list of str ]'
        return [ summarize_json(el) for el in obj ]
    elif isinstance(obj, dict):
        d = {}
        for k,v in obj.items():
            if 'type' in k:
                d[k] = v
            else:
                d[k] = summarize_json(v)
        return d
    else:
        return obj

def show_summary(filename):
    with io.open(filename, 'r') as f:
        data = json.load(f)
    data['cells'] = data['cells'][:6]
    summary = summarize_json(data)
    p = Popen('pygmentize -l json -f html -O cssclass=pygments'.split(), stdin=PIPE, stdout=PIPE)
    out, _ = p.communicate(json.dumps(summary, indent=1, sort_keys=True).encode('utf8'))
    display(HTML(out.decode('utf8')))

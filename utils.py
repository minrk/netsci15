import io
from subprocess import check_output, Popen, PIPE
from IPython.display import display, HTML

def add_style():
    style = check_output('pygmentize -S friendly -f html -a .pygments'.split()).decode('utf8')
    display(HTML('<style type="text/css">%s</style>' % style))
    

def show_ipynb(filename, limit=10, tail=False):
    add_style()
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

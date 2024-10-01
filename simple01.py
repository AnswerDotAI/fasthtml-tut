from fasthtml.common import *

app,rt = fast_app(live=true)

@rt('/')
def get():
    contents = Div(
        A('Link', href='/page'),
        Card('hi'),
    )
    return Title('simple01.py'), Container(H1('Home'), contents)

@rt('/page')
def get():
    contents = Div(
        A('Home', href='/'),
    )
    return Title('simple01.py'), Container(H1('Page'), contents)

serve()
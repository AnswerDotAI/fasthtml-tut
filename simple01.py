from fasthtml.fastapp import *

app = fast_app()
rt = app.route

@rt("/")
def get():
    contents = Div(
        A('Link', hx_get='/page'),
    )
    return Page('Home', contents)

@rt("/page")
def get():
    contents = Div(
        A('Home', hx_get='/'),
    )
    return Page('Page', contents)

from fasthtml.common import *

app = FastHTMLWithLiveReload(hdrs=(picolink,))
rt = app.route

@rt("/")
def get():
  return Title("fancy01.py"), Container(H1('FastHTML'), P("Hello World!"))

serve()
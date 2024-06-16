from fasthtml.common import *
import uvicorn

app = FastHTML()
rt = app.route

@rt("/")
def get():
  return Title("FastHTML"), H1("Hello World!")


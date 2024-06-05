from fasthtml.all import *
import uvicorn

db = database('data/todos.db')
todos = db.t.todos
if todos not in db.t: todos.create(id=int, title=str, done=bool, pk='id')
Todo = todos.dataclass()

app = FastHTML()
rt = app.route

@rt("/")
def get():
  todolist = Ul(*[Li(f'{o.title} {"✅" if o.done else ""}') for o in todos()])
  contents = Main(H1("Hello World!"), todolist)
  return Title("FastHTML"), contents


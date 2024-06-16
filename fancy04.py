from fasthtml.common import *
import uvicorn

db = database('data/todos.db')
todos = db.t.todos
if todos not in db.t: todos.create(id=int, title=str, done=bool, pk='id')
Todo = todos.dataclass()

app = FastHTML(hdrs=[picolink])
rt = app.route

def render_todo(todo):
   done = "✅" if todo.done else ""
   link = AX(todo.title, hx_get=f'/todo/{todo.id}', target_id='details')
   return Li(link, done, id=f'todo-{todo.id}')

@rt("/")
def get():
  todolist = Ul(*map(render_todo, todos()), id="todolist")
  group = Group(Input(placeholder="New Todo", name="title"), Button("Add"))
  header = Form(group, hx_post="/", target_id="todolist", hx_swap="beforeend")
  footer = Div(id="details")
  card = Card(todolist, header=header, footer=footer)
  contents = Main(H1("Hello World!"), card, cls="container")
  return Title("FastHTML"), contents

@rt("/")
def post(todo:Todo): return render_todo(todos.insert(todo))

@rt("/todo/{id}")
def delete(id:int):
   todos.delete(id)
   return '', Div(hx_swap_oob='innerHTML', id='details')

@rt("/todo/{id}")
def get(id:int):
  todo = todos[id]
  btn = Button('Delete', hx_delete=f'/todo/{id}', target_id=f'todo-{id}', hx_swap="delete")
  return P(todo.title), btn

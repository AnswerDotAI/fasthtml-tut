from fasthtml.all import *
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
   edit = AX('edit',     hx_get=f'/edit/{todo.id}', target_id='details')
   return Li(done, link, ' | ', edit, id=f'todo-{todo.id}')

def get_newinp(): return Input(placeholder="New Todo", name="title", hx_swap_oob="true", id="newtodo")
def get_footer(): return Div(hx_swap_oob='true', id="details")

@rt("/")
def get():
  todolist = Ul(*map(render_todo, todos()), id="todolist")
  header = Form(Group(get_newinp(), Button("Add")),
                hx_post="/", target_id="todolist", hx_swap="beforeend")
  card = Card(todolist, header=header, footer=get_footer())
  contents = Main(H1("Todo list"), card, cls="container")
  return Title("Todo list"), contents

@rt("/")
def post(todo:Todo): return render_todo(todos.insert(todo)), get_newinp()

@rt("/todo/{id}")
def delete(id:int):
   todos.delete(id)
   return get_footer()

@rt("/todo/{id}")
def get(id:int):
  todo = todos[id]
  btn = Button('Delete', hx_delete=f'/todo/{id}', target_id=f'todo-{todo.id}', hx_swap="delete")
  return P(todo.title), btn

@rt("/edit/{id}")
def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        hx_put="/", target_id=f'todo-{id}', id="edit")
    return fill_form(res, todos.get(id))

@rt("/")
def put(todo: Todo): return render_todo(todos.update(todo)), get_footer()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", default=8000)))

from fasthtml.common import *

db = database('data/todos.db')
todos = db.t.todos
if todos not in db.t: todos.create(id=int, title=str, done=bool, pk='id')
Todo = todos.dataclass()

app = FastHTMLWithLiveReload(hdrs=[picolink])
rt = app.route

@patch
def __ft__(self:Todo):
   done = "✅" if self.done else ""
   link = AX(self.title, hx_get=f'/todo/{self.id}', hx_target='#details')
   edit = AX('edit',     hx_get=f'/edit/{self.id}', hx_target='#details')
   return Li(done, link, ' | ', edit, id=f'todo-{self.id}')

def get_newinp(): return Input(placeholder="New Todo", name="title", hx_swap_oob="true", id="newtodo")
def get_footer(): return Div(hx_swap_oob='true', id="details")

@rt("/")
def get():
  todolist = Ul(*todos(), id="todolist")
  header = Form(Group(get_newinp(), Button("Add")),
                hx_post="/", hx_target="#todolist", hx_swap="beforeend")
  card = Card(todolist, header=header, footer=get_footer())
  contents = Main(H1("Todo list"), card, cls="container")
  return Title("Fancy - main.py"), contents

@rt("/")
def post(todo:Todo): return todos.insert(todo), get_newinp()

@rt("/todo/{id}")
def delete(id:int):
   todos.delete(id)
   return get_footer()

@rt("/todo/{id}")
def get(id:int):
  todo = todos[id]
  btn = Button('Delete', hx_delete=f'/todo/{id}', hx_target=f'#todo-{id}', hx_swap="delete")
  return P(todo.title), btn

@rt("/edit/{id}")
def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), CheckboxX(id="done", label='Done'),
        hx_put="/", hx_target=f'#todo-{id}', id="edit")
    return fill_form(res, todos.get(id))

@rt("/")
def put(todo: Todo): return todos.update(todo), get_footer()

serve()
from fasthtml.common import *
import subprocess

app,rt,todos,Todo = fast_app('data/todos.db', id=int, title=str, done=bool, pk='id', live=True)

def TodoRow(todo):
    return Li(
        A(todo.title, hx_get=f'/todos/{todo.id}', hx_target='#current-todo'),
        (' (done)' if todo.done else '') + ' | ',
        A('edit',     hx_get=f'/edit/{todo.id}', hx_target='#current-todo'),
        id=f'todo-{todo.id}'
    )

def home():
    add = Form(
            Group(
                Input(name="title", placeholder="New Todo"),
                Button("Add")
            ), hx_post="/", hx_target="body"
        )
    card = Card(
                Ul(*map(TodoRow, todos()), id='todo-list'),
                header=add,
                footer=Div(id='current-todo')
            )
    return Title('Simple - main.py'), Container(H1('Todo list'), card)

@rt("/")
def get(): return home()

@rt("/")
def post(todo:Todo):
    todos.insert(todo)
    return home()

@rt("/")
def put(todo: Todo):
    todos.update(todo)
    return home()

@rt("/")
def delete(id:int):
    todos.delete(id)
    return home()

@rt("/edit/{id}")
def get(id:int):
    res = Form(
            Group(
                Input(id="title"),
                Button("Save")
            ),
            Hidden(id="id"),
            CheckboxX(id="done", label='Done'),
            Button('Back', hx_get='/'),
            hx_put="/", hx_target='body', id="edit"
        )
    frm = fill_form(res, todos[id])
    return Container('Edit Todo', frm)

@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        P(todos[id].title),
        Button('Delete', hx_delete='/', hx_target='body', value=id, name="id"),
        Nbsp(),
        Button('Back', hx_get='/', hx_target='body')
    )
    return Container('Todo details', contents)

def serve_dev(db_path='data/todos.db', sqlite_port=8090, jupyter_port=8091, tw_src='./src/app.css', tw_dist='./public/app.css'):
    sqlite_process = subprocess.Popen(
        ['sqlite_web', db_path, '--port', str(sqlite_port), '--no-browser'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        print(f'SQLite: http://localhost:{sqlite_port}')
        serve(reload_includes=["*.css"])
    finally:
        sqlite_process.terminate()

serve_dev()
#serve()
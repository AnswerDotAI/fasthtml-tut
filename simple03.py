from fasthtml.fastapp import *

app,todos,Todo = fast_app('data/todos.db', id=int, title=str, done=bool, pk='id')
rt = app.route

def TodoRow(todo):
    return Li(
        A(todo.title, hx_get=f'/todos/{todo.id}'),
        (' (done)' if todo.done else ''),
        id=f'todo-{todo.id}'
    )

def home():
    add = Form(
            Group(
                Input(name="title", placeholder="New Todo"),
                Button("Add")
            ), hx_post="/"
        )
    card = Card(
                Ul(*map(TodoRow, todos()), id='todo-list'),
                header=add,
                footer=Div(id='current-todo')
            )
    return Page('Todo list', card)

@rt("/")
def get(): return home()

@rt("/")
def post(todo:Todo):
    todos.insert(todo)
    return home()

@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        Div(todos[id].title),
        Button('Back', hx_get='/')
    )
    return Page('Todo details', contents)

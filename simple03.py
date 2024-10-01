from fasthtml.common import *

app,rt,todos,Todo = fast_app('data/todos.db', id=int, title=str, done=bool, pk='id', live=True)

def TodoRow(todo):
    return Li(
        A(todo.title, hx_get=f'/todos/{todo.id}', hx_target='#current-todo'),
        (' (done)' if todo.done else ''),
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
    return Title('simple03.py'), Container(H1('Todo list'), card)

@rt("/")
def get(): return home()

@rt("/")
def post(todo:Todo):
    todos.insert(todo)
    return home()

@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        P(todos[id].title),
        Button('Back', hx_get='/', hx_target='body')
    )
    return Container(H2('Todo details'), contents)

serve()
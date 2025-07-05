from fasthtml.common import *

# We need to use todo_title as column name
# since title is parameter for fast_app
app,rt,todos,Todo = fast_app('data/todos.db', id=int, todo_title=str, done=bool, pk='id', live=True)

def TodoRow(todo):
    return Li(
        A(todo.todo_title, hx_get=f'/todos/{todo.id}', hx_target='#current-todo'),
        (' (done)' if todo.done else '') + ' | ',
        A('edit',     hx_get=f'/edit/{todo.id}', hx_target='#current-todo'),
        id=f'todo-{todo.id}'
    )

def home():
    add = Form(
            Group(
                Input(name="todo_title", placeholder="New Todo"),
                Button("Add")
            ), hx_post="/", hx_target="body"
        )
    card = Card(
                Ul(*map(TodoRow, todos()), id='todo-list'),
                header=add,
                footer=Div(id='current-todo')
            )
    return Title('simple04.py'), Container(H1('Todo list'), card)

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
                Input(id="todo_title"),
                Button("Save")
            ),
            Hidden(id="id"),
            CheckboxX(id="done", label='Done'),
            Button('Back', hx_get='/'),
            hx_put="/", hx_target='body', id="edit"
        )
    frm = fill_form(res, todos[id])
    return Title('simple04.py'), Container(H1('Edit Todo'), frm)

@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        P(todos[id].todo_title),
        Button('Delete', hx_delete='/', hx_target='body', value=id, name="id"),
        Nbsp(),
        Button('Back', hx_get='/', hx_target='body')
    )
    return Container(H1('Todo details'), contents)

serve()
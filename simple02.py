from fasthtml.fastapp import *

app,todos,Todo = fast_app('data/todos.db', id=int, title=str, done=bool, pk='id')
rt = app.route

@rt("/")
def get():
    todo_list = [
        Li(
            A(todo.title, hx_get=f'/todos/{todo.id}'),
            (' (done)' if todo.done else ''),
            id=f'todo-{todo.id}'
        ) for todo in todos()
    ]
    card = Card(
                Ul(*todo_list, id='todo-list'),
                header=add,
                footer=Div(id='current-todo')
            )
    return Page('Todo list', card)


@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        Div(todos[id].title),
        Button('Back', hx_get='/')
    )
    return Page('Todo details', contents)

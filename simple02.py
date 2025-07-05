from fasthtml.common import *

# We need to use todo_title as column name
# since title is parameter for fast_app
app,rt,todos,Todo = fast_app('data/todos.db', id=int, todo_title=str, done=bool, pk='id', live=true)

def seed_db():
    if len(todos()) == 0:
        todos.insert(Todo(todo_title="Buy groceries", done=False))
        todos.insert(Todo(todo_title="Finish project", done=False))
        todos.insert(Todo(todo_title="Tidy room", done=True))

# Add sample todos if the database is empty
seed_db()

@rt('/')
def get():
    todo_list = [
        Li(
            A(todo.todo_title, href=f'/todos/{todo.id}'),
            (' (done)' if todo.done else ''),
            id=f'todo-{todo.id}'
        ) for todo in todos()
    ]
    card = Card(
                Ul(*todo_list, id='todo-list'),
                header=add,
                footer=Div(id='current-todo')
            )
    return Title('simple02.py'), Container(H1('Todo list'), card)

@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        P(todos[id].todo_title),
        Button('Back', hx_get='/', hx_target='body', hx_push_url='/')
    )
    return Title('simple02.py'), Container(H1('Todo details'), contents)

serve()
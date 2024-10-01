from fasthtml.common import *

db = database('data/todos.db')
todos = db.t.todos
if todos not in db.t: todos.create(id=int, title=str, done=bool, pk='id')
Todo = todos.dataclass()

def seed_db():
    if len(todos()) == 0:
        todos.insert(Todo(title="Buy groceries", done=False))
        todos.insert(Todo(title="Finish project", done=False))
        todos.insert(Todo(title="Tidy room", done=True))

# Add sample todos if the database is empty
seed_db()

app = FastHTMLWithLiveReload(hdrs=(picolink,))
rt = app.route

@rt("/")
def get():
  todolist = Ul(*[Li(f'{o.title} {"✅" if o.done else ""}') for o in todos()])
  contents = Container(H1("Hello World!"), todolist)
  return Title("fancy02.py"), contents

serve()
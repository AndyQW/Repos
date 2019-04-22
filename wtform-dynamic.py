#Dynamic Form Composition
#This is a rare occurrence, but sometimes it’s necessary to create or modify a form dynamically in your view. This is possible by creating internal subclasses:

def my_view():
    class F(MyBaseForm):
        pass

    F.username = TextField('username')
    for name in iterate_some_model_dynamically():
        setattr(F, name, TextField(name.title()))

    form = F(request.POST, ...)
    # do view stuff

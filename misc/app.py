
def do_something(message, *args, plugs={}, output={},**kwargs):
   from random import randrange

   argstr = ' '.join(args)
   message = "Do CALC v4 String: "+str(message)+argstr
   graph = { 'tag': {'name':'function','value':'do_calc'}, 'name':'range', 'value':randrange(30)+10 }
   return { 'message': message, 'graph': graph}

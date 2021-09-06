from pyfi.client.api import Socket

do_something = Socket(name='pyfi.processors.sample.do_something')

result = do_something("Example 3 result!")

print("RESULT",result)
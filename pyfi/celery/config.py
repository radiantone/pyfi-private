from kombu import serialization

accept_content = ['pickle', 'application/x-python-serialize']
task_serializer = 'pickle'
result_serializer = 'pickle'

serialization.register_pickle()
serialization.enable_insecure_serializers()
print("CONFIG DONE")

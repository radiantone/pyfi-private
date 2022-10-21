from kombu import serialization

accept_content = [
    "json",
    "pickle",
    "application/json",
    "application/x-python-serialize",
]
task_serializer = "pickle"
result_serializer = "pickle"
serialization.register_pickle()
serialization.enable_insecure_serializers()

from default_types import *

t = TypeInteger()

print("\n".join(t.get_encode_function_definition()))
print("")
print("\n".join(t.get_decode_function_definition()))

t = TypeString()

print("\n".join(t.get_encode_function_definition()))
print("")
print("\n".join(t.get_decode_function_definition()))
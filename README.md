This project use for define your object models in applications, just example:
```python
class User(GenericSlotsObjectModel):
    all_fields = ('name', 'password_hash', 'email', 'uid', 'weight', 'status')
    optional_fields = ('weight',)
    default_values = {'status': READER_STATUS} # READER_STATUS = 0
    fields_types = {
        'name': (str,),
        'password_hash': (bytearray,),
        'email': (str,),
        'uid': (UserId,),
        'weight': (int,),
        'status': (UserStatus,)
    }

    def __init__(self, data):
        self.init_model(data)
        InCache(self.uid)

doc = mongo.FindLastUser() # doc is just simple dict

print(doc)

#{
#  'name': 'Nick',
#  'password_hash': b'smth hash',
#  'email': 'user@mail.net',
#  'uid': UserId(1234567)
#}


user = User(doc)

print(user)
# {'email': 'user@mail.net', 'status': 0, 'name': 'Nick', 'password_hash': bytearray(b'smth hash'), 'uid': '1'}

print(user.email)
# user@mail.net
```

Or like django models:
```python
class User(PrettyDictObjectModel):
    name = Field(types=(str,))
    password_hash = Field(types=(bytearray,))
    email = Field(types=(str,))
    uid = Field(types=(UserId,))
    weight = Field(types=(str,), optional=True)
    status = Field(types=(str,), default_value=READER_STATUS)

doc = mongo.FindLastUser() # doc is just simple dict

print(doc)

#{
#  'name': 'Nick',
#  'password_hash': b'smth hash',
#  'email': 'user@mail.net',
#  'uid': UserId(1234567)
#}


user = User(doc)

print(user)
# {'email': 'user@mail.net', 'status': 0, 'name': 'Nick', 'password_hash': bytearray(b'smth hash'), 'uid': '1'}

print(user.email)
# user@mail.net
```

Enjoy :)
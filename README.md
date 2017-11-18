# ObjectModeler
[![Build Status](https://travis-ci.org/KeyStorke/ObjectModeler.svg?branch=master)](https://travis-ci.org/KeyStorke/ObjectModeler)   [![PyPI version](https://badge.fury.io/py/object_modeler.svg)](https://badge.fury.io/py/object_modeler) 


ObjectModeler is an open source library for definition the data models, control a types and control a integrity of data models.

## Features
* Inheritance a fields
* Control of types
* Set default values
* Ignore of undefined fields on initialize objects
* Integrity control for models (only slots-based classes)
* Serialisation an objects in dict

## Use-cases
* Abstractions in which need validating data types and integrity a model
* Data models which need inherit
* Simply and clearly to define data types and objects schemes
* Using a slots mechanism in models for optimize and save clear code

## Install
```
pip install object_modeler
```

## Tests
```
git clone https://github.com/KeyStorke/ObjectModeler
cd ObjectModeler
python setup.py test
```

## Usage 

### Define model
```python
import time

from object_modeler import SlotsObjectModel, Field

WRITER = 0
READER = 1


class GeneralUser(SlotsObjectModel):
    uid = Field().types(str)
    name = Field(default_value='unnamed').types(str)
    status = Field(default_value=READER).types(int)
    last_online = Field(default_value=0).types(float)
    status_text = Field(optional=True).types(str)

    def is_online(self):
        return self.last_online > time.time()-60

```

### Inheritance models
Support inheritance fields and methods
``` python
class ExternalUser(GeneralUser):
    external_service = Field().types(str)
    access_token = Field().types(str)
```

### Init models from dict
Ignore (silently, without exceptions) parameters which undefined in model like `responce_id`, and control a types (`uid` will be cast to `str`).
``` python
any_dict = {
    'uid'             : 10,
    'name'            : 'Nick',
    'status'          : WRITER,
    'last_online'     : 1510920503.8094354,
    'status_text'     : 'LSS: SIN, ACK, FIN',
    'external_service': 'Github',
    'access_token'    : 'some access token'
    'responce_id'     : 'something_resp_id'
}

obj = ExternalUser(any_dict)
```

### Call a inherited method
``` python
print('User {name} (id {uid}) is online {last_online}'.format(name=obj.name,
                                                             uid=obj.uid,
                                                             last_online='NOW' if obj.is_online()
                                                             else time.ctime(obj.last_online)))
```

### Integrity control in runtime
Control integrity objects (with `__slots__` mechanism help)
``` python
obj.username = 'other name'
# AttributeError: 'ExternalUser' object has no attribute 'username'
```

For disable integrity control in runtime - use `ObjectModel`. 
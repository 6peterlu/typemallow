from marshmallow import Schema, fields
from .mappings import mappings

__schemas = dict()

def ts_interface(context='default'):
    '''

    Any valid Marshmallow schemas with this class decorator will 
    be added to a list in a dictionary. An optional parameter: 'context'
    may be provided, which will create separate dictionary keys per context.
    Otherwise, all values will be inserted into a list with a key of 'default'.

    e.g.

    @ts_interface(context='internal')
    class Foo(Schema):
        first_field = fields.Integer()

    '''
    def decorator(cls):
        if issubclass(cls, Schema):
            if isinstance(context, list):
                for ctx in context:
                    if not ctx in __schemas:
                        __schemas[ctx] = []
                    __schemas[ctx].append(cls)
            else:
                if not context in __schemas:
                    __schemas[context] = []
                __schemas[context].append(cls)
        return cls
    return decorator

def _get_ts_type(value):
    if type(value) is fields.Nested:
        ts_type = value.nested.__name__
        if value.many:
            ts_type += '[]'
    elif type(value) is fields.List:
        item_type = value.container.__class__
        if item_type is fields.Nested:
            nested_type = value.container.nested.__name__
            ts_type = f'{nested_type}[]'
        else:
            ts_type = mappings.get(item_type, 'any')
            ts_type = f'{ts_type}[]'
    elif type(value) is fields.Dict:
        keys_type = mappings.get(type(value.key_container), 'any')
        values_type = _get_ts_type(value.value_container)
        ts_type = f'{{[key: {keys_type}]: {values_type}}}'
    else:
        ts_type = mappings.get(type(value), 'any')

    return ts_type


def __get_ts_interface(schema):
    '''

    Generates and returns a Typescript Interface by iterating
    through the declared Marshmallow fields of the Marshmallow Schema class
    passed in as a parameter, and mapping them to the appropriate Typescript
    data type.

    '''
    name = schema.__name__.replace('Schema', '')
    ts_fields = []
    for key, value in schema._declared_fields.items():
        if type(value) is fields.Nested:
            ts_type = value.nested.replace('Schema', '')
            if value.many:
                ts_type += '[]'
        else:
            ts_type = _get_ts_type(value)

        ts_fields.append(
            f'\t{key}: {ts_type};'
        )
    ts_fields = '\n'.join(ts_fields)
    return f'export interface {name} {{\n{ts_fields}\n}}\n\n'


def generate_ts(output_path, context='default'):
    '''

    When this function is called, a Typescript interface will be generated
    for each Marshmallow schema in the schemas dictionary, depending on the
    optional context parameter provided. If the parameter is ignored, all
    schemas in the default value, 'default' will be iterated over and a list
    of Typescript interfaces will be returned via a list comprehension.
    
    The Typescript interfaces will then be outputted to the file provided.

    '''
    with open(output_path, 'w') as output_file:
        interfaces = [__get_ts_interface(schema) for schema in __schemas[context]]
        output_file.write(''.join(interfaces))

from marshmallow import fields

mappings = {
    fields.Bool: 'boolean',
    fields.Boolean: 'boolean',
    fields.Constant: 'any',
    fields.DateTime: 'Date',
    fields.Decimal: 'number',
    fields.Dict: 'object',
    fields.Email: 'string',
    fields.Field: 'any',
    fields.Float: 'number',
    fields.Function: 'any',
    fields.Int: 'number',
    fields.Integer: 'number',
    fields.List: 'any[]',
    fields.Mapping: 'any',
    fields.Method: 'any',
    fields.Number: 'number',
    fields.Raw: 'any',
    fields.Str: 'string',
    fields.String: 'string',
    fields.TimeDelta: 'any',
    fields.Url: 'string',
    fields.Url: 'string',
    fields.UUID: 'string',
}

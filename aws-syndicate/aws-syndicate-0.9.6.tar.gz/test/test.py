syndicate = {
    "resource_type": "dynamodb_table",
    "hash_key_name": "id",
    "hash_key_type": "S",
    "sort_key_name": "name",
    "sort_key_type": "S",
    "read_capacity": 2,
    "write_capacity": 1,
    "indexes": {
        'a': 'sda'
    }
}
aws = {
    "resource_type": "dynamodb_table",
    "hash_key_name": "ids",
    "hash_key_type": "B",
    "sort_key_name": "name",
    "sort_key_type": "B",
    "read_capacity": 2,
    "write_capacity": 1,
    "indexes": {
        'b': 'sda'
    }

}

errors_set = set(syndicate.items()) ^ set(aws.items())  # get difference between two dicts
keys_with_errors = {i[0] for i in errors_set}
print(keys_with_errors)
result = {}
for key in keys_with_errors:
    expected_value = syndicate.get(key)
    actual_value = aws.get(key)
    result[key] = (expected_value, actual_value)

print(errors_set)
print(result)
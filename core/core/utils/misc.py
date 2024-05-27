import yaml


def yaml_coerce(data):
    if isinstance(data, str):
        return yaml.load(f"dummy: {data}", Loader=yaml.SafeLoader)["dummy"]
    return data

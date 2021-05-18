import json


def write_settings(section, key, value, mode='write'):
    with open('settings/' + section, 'r+') as fp:
        option = json.load(fp)
        if mode == 'write':
            option[key] = value
        elif mode == 'update':
            option[key].update(value)
        else:
            return
        fp.seek(0)
        fp.truncate()
        json.dump(option, fp, indent=2)


def get_settings(section, key, fallback=''):
    with open('settings/' + section, 'r') as f:
        try:
            value = json.load(f)[key]
        except KeyError:
            # If value doesn't exist
            value = fallback
            write_settings(section, key, fallback)
        return value

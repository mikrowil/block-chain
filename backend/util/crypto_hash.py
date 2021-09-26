import hashlib
import json


def stringify(data):
    return json.dumps(data)


def crypto_hash(*data):
    """
    :param data:
    :return: s sha-256 hash for the data
    """
    str_data = map(lambda x: json.dumps(x), data)
    joined_data = ''.join(str_data)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f'crypto_hash([2, 5, 6, 7]): {crypto_hash([2, 5, 6, 7])}')


if __name__ == '__main__':
    main()

import yaml


class MutatedDict(dict):
    """Class used to mark dictionary values that have been mutated.

    In general, Cels uses references to the original and patch dictionaries and lists
    to build the final patched result. However, when one of those dictionaries or lists
    is modified in place, a shallow copy is used instead in order not to modify the original
    data structure. For dictionaries, the shallow copy will be marked as mutated by using this class.
    """

    pass


def mutated_dict_representer(dumper, data):
    return dumper.represent_dict(data)


yaml.add_representer(MutatedDict, mutated_dict_representer, Dumper=yaml.SafeDumper)

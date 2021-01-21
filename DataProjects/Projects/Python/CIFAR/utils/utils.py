import argparse

# To decode the files
import pickle

def get_args():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-c', '--config',
        metavar='C',
        default='None',
        help='The Configuration file')
    args = argparser.parse_args()
    return args


    def get_class_names():
        # Load class names
        raw = unpickle("batches.meta")[b'label_names']

        # Convert from binary strings
        names = [x.decode('utf-8') for x in raw]

        # Class names
        return names

from src.store.arg_parser.arg_parser import arg_parser
from src.store.Datastore import Datastore


def main():
    args = arg_parser()
    datastore = Datastore()
    datastore.process(args.key_name, args.action, args.valueOrVersion)

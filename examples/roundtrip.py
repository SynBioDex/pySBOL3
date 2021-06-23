import argparse
import logging
import pathlib

import rdflib.util

import sbol3

# Round trip a directory tree of SBOL3 files, creating a parallel tree
# containing the output files.


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("in_dir", metavar="INPUT_DIR")
    parser.add_argument("out_dir", metavar="OUTPUT_DIR")
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-e', '--extension', metavar="FILE_EXTENSION",
                        default='ttl')
    parser.add_argument('-v', '--validate', action='store_true')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s|%(levelname)s|%(message)s'
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def round_trip_file(in_file, out_file, validate=False):
    # Determine RDF file format
    file_format = rdflib.util.guess_format(in_file)
    doc = sbol3.Document()
    logging.info(f'Reading {in_file}')
    doc.read(str(in_file), file_format=file_format)
    if validate:
        report = doc.validate()
        if report:
            logging.warning(f'Found {len(report)} validation errors')
    logging.info(f'Writing {out_file}')
    doc.write(str(out_file), file_format=file_format)


def main(argv=None):
    args = parse_args(argv)
    # Init logging
    init_logging(args.debug)
    logging.debug('Starting')
    root_dir = pathlib.Path(args.in_dir)
    out_dir = pathlib.Path(args.out_dir)
    for in_file in root_dir.rglob(f'*.{args.extension}'):
        # Determine output file
        out_file = out_dir / in_file.relative_to(root_dir)
        # Create parent directories of output file
        out_file.parent.mkdir(parents=True, exist_ok=True)
        round_trip_file(in_file, out_file, validate=args.validate)
    logging.debug('Done')


if __name__ == '__main__':
    main()

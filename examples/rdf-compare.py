import argparse
import logging
import pathlib

import rdflib.util
import rdflib.compare

# Compare two RDF files or two parallel RDF directory trees
#
# This is used to compare SBOL3 files without using pySBOL3
# in order to determine if the files contain the same triples.
# If any files differ the differences are logged at WARNING level.


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('in1', metavar='INPUT_1')
    parser.add_argument('in2', metavar='INPUT_2')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s|%(levelname)s|%(message)s'
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def compare_files(file1, file2):
    # Now compare the graphs in RDF
    g1 = rdflib.Graph()
    g1.parse(file1.as_posix(), format=rdflib.util.guess_format(file1.as_posix()))
    iso1 = rdflib.compare.to_isomorphic(g1)
    g2 = rdflib.Graph()
    g2.parse(file2.as_posix(), format=rdflib.util.guess_format(file2.as_posix()))
    iso2 = rdflib.compare.to_isomorphic(g2)
    rdf_diff = rdflib.compare.graph_diff(iso1, iso2)
    if rdf_diff[1] or rdf_diff[2]:
        logging.warning('Detected %d different RDF triples in %s' %
                        (len(rdf_diff[1]) + len(rdf_diff[2]), file1))
        for stmt in rdf_diff[1]:
            logging.warning('Only in %s: %r', file1, stmt)
        for stmt in rdf_diff[2]:
            logging.warning('Only in %s: %r', file2, stmt)


def compare_tree(dir1, dir2):
    """Compare all the files in the two directory trees.
    """
    # iterate over all the files in dir1
    for path1 in dir1.glob('**/*'):
        if not path1.is_file():
            continue
        logging.debug(path1)
        path2 = dir2 / path1.relative_to(dir1)
        compare_files(path1, path2)


def main(argv=None):
    args = parse_args(argv)
    # Init logging
    init_logging(args.debug)
    logging.debug('Starting')
    in1 = pathlib.Path(args.in1)
    in2 = pathlib.Path(args.in2)
    if in1.is_dir():
        compare_tree(in1, in2)
    else:
        compare_files(in1, in2)
    logging.debug('Done')


if __name__ == '__main__':
    main()

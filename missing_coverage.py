import json
import sys

from argparse import ArgumentParser


def skipfile(file, startswith, endswith, patterns):
    for text in startswith:
        if file.startswith(text):
            return True

    for text in endswith:
        if file.endswith(text):
            return True

    for text in patterns:
        try:
            if file.index(text) >= 0:
                return True
        except:
            pass
    return False


def main(args=sys.argv[1:]):
    parser = ArgumentParser()
    parser.add_argument('--json', required=True,
                        help="json map of coverage jobs.")
    parser.add_argument('--changesets', required=True,
                        help="json of hg changesets + files changed.")
    args = parser.parse_args(args)

    with open(args.json, 'r') as f:
        coverage_map = json.load(f)

    with open(args.changesets, 'r') as f:
        changesets = json.load(f)

    all_missing = []
    for rev in changesets:
        missing = []
        matched = 0
        total_files = 0
        for file in changesets[rev]:
             total_files += 1
             # Known lack of coverage
             startswith = ['servo', 'mobile', 'third_party']
             endswith = ['.java', '.rs', '.mm', '.nsi', '.nsh']
             if skipfile(file, startswith, endswith, []):
                 continue

             # Typically testing
             startswith = ['testing', 'taskcluster']
             endswith = ['.ini', '.list', '.html', '.xul', '.py', '.yml']
             pattern = ['test']
             if skipfile(file, startswith, endswith, pattern):
                 continue

             # build/tooling
             startswith = ['build', 'config']
             endswith = ['.build', '.mozbuild', '.mn', '.rdf', '.rdf.in', '.mk',
                         '.dep', '.lock', '.sh', '.conf', 'package-manifest.in', 'MacOS-files.in']
             pattern = ['configure', 'akefile', 'mozconfig']
             if skipfile(file, startswith, endswith, pattern):
                 continue

             # Extra files
             startswith = ['build', 'config']
             endswith = ['.css', '.svg', '.xml', '.xhtml', '.ico', '.jpg', '.png',
                         '.bmp', '.properties', '.dtd', '.mozilla', '.json', '.inc',
                         '.manifest', '.errors', '.yaml', '.rst', '.dic', '.glsl',
                         '.toml', '.d', 'TAG-INFO', '.idl', '.webidl', '.ipdl']
             pattern = ['README']
             if skipfile(file, startswith, endswith, pattern):
                 continue

             # Missing from coverage for right now
             startswith = []
             endswith = ['.js', '.jsm']
             pattern = []
#             if skipfile(file, startswith, endswith, pattern):
#                 continue

             # hacking out for current dataset:
             startswith = []
             endswith = []
             pattern = ['gfx/harfbuzz', 'netwerk/streamconv/converters/parse-ftp']
             if skipfile(file, startswith, endswith, pattern):
                 continue

             # files we detect, use this to get ideas of patterns of other file types to reduce noise
             startswith = []
             endswith = ['.cpp', '.h', '.cc']
             pattern = []
             if skipfile(file, startswith, endswith, pattern):
                 continue

             if file not in coverage_map:
                 missing.append(file)
                 if file not in all_missing:
                     all_missing.append(file)
             else:
                 matched += 1

        if missing:
            print "%s: %s, %s" % (rev, matched, missing)
        elif matched > 0 and matched != total_files:
            print "%s: %s/%s" % (rev, matched, total_files)

    all_missing.sort()
    print len(all_missing)

if __name__ == "__main__":
    main()

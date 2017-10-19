import json
import subprocess

def main():
    p = subprocess.Popen('hg log -l 10', shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]

    changesets = []
    for line in output.split('\n'):
        if line.startswith('changeset'):
            parts = line.split(':')
            changesets.append(parts[-1])

    retVal = {}
    for c in changesets:
        if not c:
            continue
        retVal[c] = []
        p = subprocess.Popen('hg status -n --change %s' % c, shell=True, stdout=subprocess.PIPE)
        output = p.communicate()[0]

        for line in output.split('\n'):
            line = line.strip()
            line = line.replace('\\', '/')
            if not line:
                continue
            retVal[c].append(line)

    with open('changes_files.json', 'wb') as f:
        json.dump(retVal, f)


if __name__ == "__main__":
    main()

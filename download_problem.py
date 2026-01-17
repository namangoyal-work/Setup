#!/usr/bin/env python3
"""Download and setup problems from Competitive Companion

Usage:
  download_problem.py [options] [<name>...]

Options:
  -h --help                  Show this screen.
  --echo                     Just echo received responses and exit.
  --dryrun                   Don't actually create any problems.
  -n COUNT, --number COUNT   Number of problems to listen for.
  -b COUNT, --batches COUNT  Number of batches to listen for.
  -t TIME, --timeout TIME    Timeout for listening (in seconds).
"""

from docopt import docopt
import sys
import http.server
import json
from pathlib import Path
import subprocess
import re

# Returns unmarshalled data or None
def listen_once(*, timeout=None):
    json_data = None

    class CompetitiveCompanionHandler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            nonlocal json_data
            json_data = json.load(self.rfile)
        # Suppress default logging
        def log_message(self, format, *args):
            return

    try:
        # Port 10046 is the default for Competitive Companion
        with http.server.HTTPServer(('127.0.0.1', 10046), CompetitiveCompanionHandler) as server:
            server.timeout = timeout
            server.handle_request()
    except OSError as e:
        print(f"Error: Could not bind to port 10046. Is another instance running? ({e})")
        return None

    if json_data is not None:
        print(f"Received problem: {json_data.get('name', 'Unknown')}")
    else:
        print("Timeout or no data received.")
    return json_data

def listen_many(*, num_items=None, num_batches=None, timeout=None):
    # Case 1: Listen for specific count of problems
    if num_items is not None:
        res = []
        for i in range(num_items):
            print(f"Waiting for problem {i+1}/{num_items}...")
            cur = listen_once(timeout=None)
            if cur: res.append(cur)
        return res

    # Case 2: Listen for batches (e.g. a whole contest)
    if num_batches is not None:
        res = []
        batches = {}
        # Keep listening until we satisfy the number of batches
        while len(batches) < num_batches or any(need > 0 for need, tot in batches.values()):
            print(f"Listening for data... (Batches needed: {num_batches})")
            cur = listen_once(timeout=None)
            if not cur: break
            
            res.append(cur)
            cur_batch = cur['batch']
            batch_id = cur_batch['id']
            batch_cnt = cur_batch['size']
            
            if batch_id not in batches:
                batches[batch_id] = [batch_cnt, batch_cnt]
            
            batches[batch_id][0] -= 1
            print(f"  - Batch {batch_id[:8]}...: {batches[batch_id][1] - batches[batch_id][0]}/{batches[batch_id][1]} problems received")

        return res

    # Case 3: Default loop (listen until timeout or manual stop)
    res = [listen_once(timeout=None)] # Wait indefinitely for the first one
    while True:
        # After the first one, use a short timeout to catch others in the same burst
        cnd = listen_once(timeout=timeout if timeout else 2.0)
        if cnd is None:
            break
        res.append(cnd)
    return res

NAME_PATTERN = re.compile(r'^(?:Problem )?([A-Z][0-9]*)\b')

def get_prob_name(data):
    # Special handling for USACO
    if 'USACO' in data['group']:
        if 'fileName' in data['input']:
            names = [data['input']['fileName'].rstrip('.in'), data['output']['fileName'].rstrip('.out')]
            if len(set(names)) == 1:
                return names[0]

    # Special handling for CodeChef
    if 'url' in data and data['url'].startswith('https://www.codechef.com'):
        return data['url'].rstrip('/').rsplit('/')[-1]

    # Heuristic: Match "A", "B", "C1" from the name
    patternMatch = NAME_PATTERN.search(data['name'])
    if patternMatch is not None:
        return patternMatch.group(1)

    # Fallback: Ask user
    print(f"Could not auto-detect simple name for: {data['name']}")
    return input("Enter short name (e.g. A, B): ").strip()

def save_samples(data, prob_dir):
    with open(prob_dir / 'problem.json', 'w') as f:
        json.dump(data, f, indent=2)

    for i, t in enumerate(data['tests'], start=1):
        with open(prob_dir / f'sample{i}.in', 'w') as f:
            f.write(t['input'])
        with open(prob_dir / f'sample{i}.out', 'w') as f:
            f.write(t['output'])

def make_prob(data, name=None):
    if name is None:
        name = get_prob_name(data)

    # Sanitize name to be safe for file systems
    name = "".join(x for x in name if x.isalnum() or x in "._-")
    prob_dir = Path('.') / name

    if prob_dir.exists() and prob_dir.is_dir():
        print(f"Skipping {name}: Folder already exists.")
    else:
        print(f"Creating problem {name}...")
        # Find make_prob.sh in the same directory as this script
        MAKE_PROB = Path(sys.path[0]) / 'make_prob.sh'
        
        try:
            subprocess.check_call([str(MAKE_PROB), name], stdout=sys.stdout, stderr=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error executing make_prob.sh: {e}")
            return
        except FileNotFoundError:
             print(f"Error: Could not find make_prob.sh at {MAKE_PROB}")
             return

    print(f"Saving samples to {name}/...")
    save_samples(data, prob_dir)
    print("Done.\n")

def main():
    arguments = docopt(__doc__)

    if arguments['--echo']:
        print("Echo mode enabled. Listening...")
        while True:
            listen_once()
    else:
        dryrun = arguments['--dryrun']
        
        def run_make_prob(data, name=None):
            if dryrun:
                print(f"[Dry Run] Would create problem: {data['name']}")
                return
            make_prob(data, name)

        # Logic to determine how many items to listen for
        datas = []
        if names := arguments['<name>']:
            print(f"Listening for {len(names)} specific problems...")
            datas = listen_many(num_items=len(names))
            for data, name in zip(datas, names):
                run_make_prob(data, name)
        
        elif cnt := arguments['--number']:
            print(f"Listening for {cnt} problems...")
            datas = listen_many(num_items=int(cnt))
            for data in datas:
                run_make_prob(data)
        
        elif batches := arguments['--batches']:
            # Default batch count is 1 if not specified, but docopt handles the flag
            b_cnt = int(batches) if batches else 1
            print(f"Listening for {b_cnt} batches (e.g. contests)...")
            datas = listen_many(num_batches=b_cnt)
            for data in datas:
                run_make_prob(data)
                
        elif timeout := arguments['--timeout']:
            print(f"Listening with timeout {timeout}s...")
            datas = listen_many(timeout=float(timeout))
            for data in datas:
                run_make_prob(data)
                
        else:
            # DEFAULT BEHAVIOR (No args)
            # Listen for 1 batch (usually 1 contest or 1 problem set sent at once)
            print("Listening for incoming problems (Ctrl+C to stop)...")
            datas = listen_many(num_batches=1)
            for data in datas:
                run_make_prob(data)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped the competitive companion listening service.")

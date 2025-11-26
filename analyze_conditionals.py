import os
import re

def analyze_conditionals(directory):
    files = sorted([f for f in os.listdir(directory) if f.endswith('.tex')])
    
    dangling_ifs = {}
    starting_fis = {}
    starting_ifs = {}
    
    for filename in files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for dangling ifs at the end (last 500 chars)
        # We look for \if... that is not closed by \fi
        # This is a simple heuristic
        
        # Better: check the very last non-whitespace lines
        lines = content.strip().split('\n')
        if not lines: continue
        
        last_lines = lines[-5:]
        for line in last_lines:
            if re.search(r'\\if[a-zA-Z]+', line) and not re.search(r'\\fi', line):
                dangling_ifs[filename] = line.strip()
                
        # Check for starting fi (first 5 lines)
        first_lines = lines[:5]
        for line in first_lines:
            if re.search(r'^\s*\\fi', line):
                starting_fis[filename] = line.strip()
            if re.search(r'^\s*\\if[a-zA-Z]+', line):
                starting_ifs[filename] = line.strip()

    print("Dangling IFs (at end of file):")
    for f, l in dangling_ifs.items():
        print(f"{f}: {l}")
        
    print("\nStarting FIs (at start of file):")
    for f, l in starting_fis.items():
        print(f"{f}: {l}")

    print("\nStarting IFs (at start of file):")
    for f, l in starting_ifs.items():
        print(f"{f}: {l}")

if __name__ == "__main__":
    analyze_conditionals('capitulos')

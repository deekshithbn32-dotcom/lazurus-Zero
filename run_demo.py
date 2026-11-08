import os
import sys

# Forward to inner Lazarus-Zero directory
inner_dir = os.path.join(os.path.dirname(__file__), "Lazarus-Zero")
if os.path.exists(inner_dir):
    os.chdir(inner_dir)
    sys.path.insert(0, inner_dir)
    import run_demo
    run_demo.main()
else:
    print("Error: Lazarus-Zero directory not found.")

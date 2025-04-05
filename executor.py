import sys
import subprocess
import os

lang = sys.argv[1]
filename = sys.argv[2]

def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=10, input=sys.stdin.read())
        print(output)
    except subprocess.CalledProcessError as e:
        print(e.output)
    except subprocess.TimeoutExpired:
        print("Error: Execution timed out.")

if lang == "c":
    out_file = "a.out"
    compile_cmd = ["gcc", filename, "-o", out_file]
    run_command(compile_cmd)
    run_command([f"./{out_file}"])

elif lang == "cpp":
    out_file = "a.out"
    compile_cmd = ["g++", filename, "-o", out_file]
    run_command(compile_cmd)
    run_command([f"./{out_file}"])

elif lang == "py":
    run_command(["python3", filename])

elif lang == "js":
    run_command(["node", filename])

elif lang == "java":
    compile_cmd = ["javac", filename]
    run_command(compile_cmd)
    class_name = os.path.splitext(os.path.basename(filename))[0]
    run_command(["java", class_name])

elif lang == "go":
    run_command(["go", "run", filename])

else:
    print(f"Unsupported language: {lang}")

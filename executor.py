import sys
import subprocess
import os

def run_command(cmd, input_data=None):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=10, input=input_data)
        return output
    except subprocess.CalledProcessError as e:
        return e.output
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 executor.py <language> <filename>")
        sys.exit(1)

    lang = sys.argv[1]
    filename = sys.argv[2]
    
    input_data = sys.stdin.read() if not sys.stdin.isatty() else None
    
    result = ""
    
    if lang == "c":
        out_file = os.path.join(os.path.dirname(filename), "a.out")
        compile_cmd = ["gcc", filename, "-o", out_file]
        result += run_command(compile_cmd)
        if os.path.exists(out_file):
            result += run_command([out_file], input_data)
    
    elif lang == "cpp":
        out_file = os.path.join(os.path.dirname(filename), "a.out")
        compile_cmd = ["g++", filename, "-o", out_file]
        result += run_command(compile_cmd)
        if os.path.exists(out_file):
            result += run_command([out_file], input_data)
    
    elif lang == "py":
        result = run_command(["python3", filename], input_data)
    
    elif lang == "js":
        result = run_command(["node", filename], input_data)
    
    elif lang == "java":
        with open(filename, 'r') as f:
            content = f.read()
        
        class_name = os.path.splitext(os.path.basename(filename))[0]
        compile_cmd = ["javac", filename]
        result += run_command(compile_cmd)
        
        file_dir = os.path.dirname(filename)
        run_dir = file_dir if file_dir else "."
        
        result += run_command(["java", "-cp", run_dir, class_name], input_data)
    
    elif lang == "go":
        result = run_command(["go", "run", filename], input_data)
    
    else:
        result = f"Unsupported language: {lang}"
    
    print(result)

if __name__ == "__main__":
    main()
import subprocess

class BashShell:
    def __init__(self):
        # Start a subprocess with bash
        self.process = subprocess.Popen(
            ["/bin/bash"], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
    
    def send_command(self, command):
        # Send a command to the bash shell
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()  # Ensure the command is sent
        
        # Read the output until the prompt returns
        output = []
        line = self.process.stdout.readline()
        while line:
            output.append(line)
            line = self.process.stdout.readline()
        return ''.join(output)

    def close(self):
        # Close the stdin to signal that no more input will be sent
        self.process.stdin.close()
        # Terminate the process
        self.process.terminate()
        # Wait for the process to finish
        self.process.wait()
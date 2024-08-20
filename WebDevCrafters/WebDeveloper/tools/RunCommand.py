import os
import signal
import socket
import platform
import subprocess
from typing import Literal
from pydantic import Field
from agency_swarm.tools import BaseTool
import threading


class RunCommand(BaseTool):
    """Enables you to execute certain terminal commands."""
    command: Literal['build', 'run-dev', 'create-next-app', 'install'] = Field(...,
                                                                    description='The terminal command to execute. Create a new Next.js app with `create-next-app`, build the current app with `build`, run a development server with `run-dev`, or install dependencies with `install`.'
                                                                    )
    options: str = Field(
        default='',
        description='Additional options to pass to the command. For example, you can pass package names to install with `npm install`.',
        examples=['--save', '--save-dev', "mui --save", 'my-next-app']
    )

    def run(self):
        try:
            options_list = [option for option in self.options.split(' ') if option]

            if self.command == 'create-next-app':
                if len(options_list) == 0:
                    return 'Please provide a name for the app when using the `create-next-app` command.'

                app_name = options_list[0]  # Extract app name from the options
                if self._shared_state.get('app_directory'):
                    return 'You have already created a Next.js app.'

                # If this command fails, ensure that nodejs folder is included in your system Path variable (for Windows)
                cmd = [
                    'npx', 'create-next-app', app_name, '--use-npm', '--ts',
                    '--no-eslint', '--no-tailwind', '--src-dir', '--no-app', '--import-alias', '@/*'
                ]

                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

                # install react-serialize
                cmd = ['npm', 'install', 'react-serialize']
                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

                if process.returncode == 0:
                    app_directory = os.path.join(os.getcwd(), app_name)
                    self._shared_state.set('app_directory', app_directory)
                    return f'Command executed successfully. App directory: {app_directory}\nOutput:\n{process.stdout} The application uses typescript. Remember to remove default content from index.tsx file.'
                else:
                    return f'Error executing command: {process.stderr}'

            # Ensures an app has been created before proceeding with 'build' or 'install'
            if not self._shared_state.get('app_directory'):
                return 'Please create a Next.js app first using the `create-next-app` command.'

            # Change to the app directory before running 'build' or 'install'
            current_directory = os.getcwd()
            os.chdir(self._shared_state.get('app_directory'))

            if self.command == 'build':
                cmd = ['npm', 'run', 'build'] + options_list
                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, timeout=30)

            
            elif self.command == 'run-dev':
                if self.is_port_in_use(3000):
                    return "Server is already running."
                
                cmd = ['npm', 'run', 'dev'] + options_list
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                # Lists to store output and errors
                stdout_lines = []
                stderr_lines = []

                # Create threads to handle stdout and stderr
                threading.Thread(target=self.stream_output, args=(process.stdout, stdout_lines)).start()
                threading.Thread(target=self.stream_output, args=(process.stderr, stderr_lines)).start()
                
                os.chdir(current_directory)
                return "Development server started."

            elif self.command == 'install':
                # For 'npm install', options might include package names or flags
                cmd = ['npm', 'install'] + options_list
                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            else:
                return 'Invalid command. Please use either `create-next-app`, `build`, or `install`.'

            os.chdir(current_directory)  # Ensure the directory is switched back

            # Return the full output of 'build' or 'install'
            return f'Command executed successfully. Output:\n{process.stdout.decode()}'

        except subprocess.CalledProcessError as e:
            if self.command == 'build':
                return f'Error building the app: {e.stderr}.\n\nPlease make sure to read the problematic file with the FileReader tool and fix the errors. If issue is related to the missing libraries, run install command first. Rewrite the entire file with FileWriter tool if you get stuck.'
            return f'Error executing command: {e.stderr}'
        
    def stream_output(self, pipe, output_list):
        for line in iter(pipe.readline, b''):
            decoded_line = line.decode()
            output_list.append(decoded_line)
            print(decoded_line, end='')
        
    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":
    tool = RunCommand(
        command="build",
        # options="travel-website"
    )
    tool._shared_state.set("app_directory", "D:\\work\\VRSEN\\code\\agency-swarm-lab\\WebDevCrafters\\webdevcrafters-app")

    print(tool.run())
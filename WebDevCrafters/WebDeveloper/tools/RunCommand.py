import os
import subprocess
import time
from typing import Literal
from pydantic import Field
from agency_swarm.tools import BaseTool


class RunCommand(BaseTool):
    """Enables you to execute certain terminal commands."""
    command: Literal['build', 'create-next-app', 'install'] = Field(...,
                                                                    description='The terminal command to execute. Create a new Next.js app with `create-next-app`, build the current app with `build`, or install dependencies with `install`.'
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
                if self.shared_state.get('app_directory'):
                    return 'You have already created a Next.js app.'

                cmd = [
                    'npx', 'create-next-app', app_name, '--use-npm', '--ts',
                    '--no-eslint', '--no-tailwind', '--src-dir', '--no-app', '--import-alias', '@/*'
                ]

                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if process.returncode == 0:
                    app_directory = os.path.join(os.getcwd(), app_name)
                    self.shared_state.set('app_directory', app_directory)
                    return f'Command executed successfully. App directory: {app_directory}\nOutput:\n{process.stdout} The application uses typescript.'
                else:
                    return f'Error executing command: {process.stderr}'

            # Ensures an app has been created before proceeding with 'build' or 'install'
            if not self.shared_state.get('app_directory'):
                return 'Please create a Next.js app first using the `create-next-app` command.'

            # Change to the app directory before running 'build' or 'install'
            current_directory = os.getcwd()
            os.chdir(self.shared_state.get('app_directory'))

            if self.command == 'build':
                cmd = ['npm', 'run', 'build'] + options_list
                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            elif self.command == 'install':
                # For 'npm install', options might include package names or flags
                cmd = ['npm', 'install'] + options_list
                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            else:
                return 'Invalid command. Please use either `create-next-app`, `build`, or `install`.'

            os.chdir(current_directory)  # Ensure the directory is switched back

            # Return the full output of 'build' or 'install'
            return f'Command executed successfully. Output:\n{process.stdout.decode()}'

        except subprocess.CalledProcessError as e:
            if self.command == 'build':
                return f'Error building the app: {e.stderr}.\n\nPlease make sure to read the problematic file with the FileReader tool and fix the errors. Rewrite the entire file with FileWriter tool if you get stuck.'
            return f'Error executing command: {e.stderr}'

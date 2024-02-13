from agency_swarm import BaseTool


class CheckCurrentDir(BaseTool):
    """
    This tool checks the current directory.
    """

    def run(self):
        import os

        if not self.shared_state.get('app_directory'):
            return "You must create an app first to use this tool."

        return os.getcwd()

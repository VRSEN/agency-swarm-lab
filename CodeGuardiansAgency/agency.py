from agency_swarm import Agency
from ReportGenerator import ReportGenerator
from CodeAnalyzer import CodeAnalyzer
from CEO import CEO

from dotenv import load_dotenv
load_dotenv()

ceo = CEO()
code_analyzer = CodeAnalyzer()
report_generator = ReportGenerator()

agency = Agency([ceo, [ceo, code_analyzer],
                 [code_analyzer, report_generator]],
                shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    print(agency.get_completion("Please analyze the code and generate a report.",
                                yield_messages=False))
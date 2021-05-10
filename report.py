from engine import Rule, Engine
from fetchdata import load_data
from process_data import process_data
from rules import *

def main():
    symbols = ['BABA', 'BILI', 'JD', 'BIDU', 'PDD', 'NIO', 'XPEV']
    engine = Engine()
    engine.add_rule(LoadDataRule(symbols))
    engine.add_rule(ProcessDataRule())
    engine.add_rule(SubjectGenerator())
    engine.add_rule(ChangeSort())
    engine.add_rule(ChangeContent())
    result = engine.run()
    print(result['subject'])
    print(result['content'])


if __name__ == '__main__':
    main()

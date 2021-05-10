class Rule:
    def process(self, context):
        pass


class Engine:
    def __init__(self):
        self.rules = []
        self.context = {}
    
    def add_rule(self, rule:Rule):
        self.rules.append(rule)

    def run(self):
        context = {}
        for rule in self.rules:
            rule.process(context)
        return context

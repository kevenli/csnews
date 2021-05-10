from engine import Rule, Engine
from fetchdata import load_data
from process_data import process_data

class LoadDataRule(Rule):
    def __init__(self, symbols):
        self.symbols = symbols

    def process(self, context):
        raw_data = {}
        for symbol in self.symbols:
            raw_data[symbol] = load_data(symbol)
        context['raw_data'] = raw_data

class ProcessDataRule():
    def process(self, context):
        data = {}
        last_price = {}
        for symbol, raw_data in context['raw_data'].items():
            symbol_data = process_data(symbol)
            # 加工后的数据集，按symbol保存
            data[symbol] = symbol_data

            # 最新价格信息，按symbol保存
            last_price[symbol] = symbol_data.iloc[-1]
            
        context['data'] = data
        context['last_price'] = last_price


class SubjectGenerator():
    def process(self, context):
        total = 0
        upper_count = 0
        for symbol, last_price in context['last_price'].items():
            total += 1
            if last_price['Chg'] > 0:
                upper_count += 1

        subject = ''
        if upper_count / total < 0.2:
            subject = '热门中概股普遍下跌'
        elif 0.2 < upper_count / total < 0.4:
            subject = '热门中概股多数下跌'
        elif 0.4 < upper_count / total < 0.6:
            subject = '热门中概股涨跌不一'
        elif 0.6 < upper_count / total < 0.8:
            subject = '热门中概股多数上涨'
        else:
            subject = '热门中概股普遍上涨'
        context['subject'] = subject


class ChangeSort():
    def process(self, context):
        asc_list = []
        desc_list = []
        chg_list = []
        for symbol, last_price in context['last_price'].items():
            chg_list.append((symbol, last_price['Chg']))
        
        asc_list = sorted(chg_list, key=lambda x:x[1])
        desc_list = sorted(chg_list, key=lambda x:x[1], reverse=True)
        context['asc_list'] = asc_list
        context['desc_list'] = desc_list


class ChangeContent():
    def process(self, context):
        content = context.get('content', '')
        asc_list = context.get('asc_list', [])
        dest_list = context.get('dest_list', [])
        if asc_list and asc_list[0][1] < 0:
            symbol, chg = asc_list[0]
            content += f'跌幅最高为{symbol}{chg*100:.1f}%,'

        if asc_list and asc_list[-1][1] > 0:
            symbol, chg = asc_list[-1]
            content += f'涨幅最高为{symbol}{chg*100:.1f}%.'

        context["content"] = content


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

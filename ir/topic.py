from bs4 import BeautifulSoup

class Topic:
    def __init__(self, topicsfile):
        with open(topicsfile, 'r', encoding='utf8') as f:
            self.raw = BeautifulSoup(f.read(), 'lxml')
        self._process()

    def _process(self):
        self.topics = []
        for i in range(1,31):
            tag = self.raw.find('topic', {"number":i})
            self.topics.append(
                {"number":i ,"disease":tag.disease.text, "gene":tag.gene.text, "demographic":tag.demographic.text}
            )

    def __getitem__(self, key):
        return self.topics[key]


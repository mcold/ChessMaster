from pathlib import Path
from os import sep
import re


class Gingko:

    def __init__(self, id: str = None, block: str = None, steps: list = None):
        self.id = id
        self.block = re.sub(r'(?<=\{).*?(?=\})', '', block).replace('{}', '')
        self.childs = list()
        self.tags = list()
        self.steps = list()
        if steps:
            self.steps = steps
        else:
            self.get_steps()
        
    def __str__(self):
        return 'id: {id}\n\n{block}\n'.format(id=self.id, block=self.block)

    def __repr__(self) -> str:
        res = '<gingko-card id="{id}">'.format(id=self.id)
        # TODO: wrap each line in ``
        res += '\n\n{block}\n\n'.format(block=self.block)
        for tag in self.tags: res += '`#{tag}`\n'.format(tag=tag)
        res += ''.join([x.__repr__() for x in self.childs])
        res += '</gingko-card>\n'
        return res
    

    def __add__(self, other: object):
        for i in range(len(self.steps)):
            other_step = self.steps.pop()
            if self.steps[i] != other_step:
                # make split
                g_new = Gingko(steps=self.steps[i:])
                # TODO: gen new id
                self.steps = self.steps[:i]
                g_new.childs = self.childs
                self.childs = [g_new, other]
                return self
        for child in self.childs:
            if child[0] == other[0]: return child + other
        self.childs.append(other)
        return self

    def __eq__(self, other: object) -> bool:
        # TODO: not only current Gingko but also childs to compare with
        if self.steps == other.steps: 
            True
        else:
            False
    
    # TODO: add method for generation in format useful in Lichess

    def gen_ids(self, init_id: str = None, parent_id: str = None) -> None:
        if not parent_id: parent_id = ''
        if not self.id and not init_id: self.id = '1'
        if not self.id and init_id: self.id = parent_id + init_id
        for i in range(len(self.childs)):
            child = self.childs[i]
            child.gen_ids(init_id = i+1, parent_id = self.id)
            

    def get_result(self, s: str) -> str:
        if s.find('1-0'): return '1-0'
        if s.find('1-0'): return '0-1'
        return None

    def get_steps(self) -> None:
        self.steps = [x.strip() for x in re.split(r'\d*\.', self.block) if x]
        result = self.get_result(self.steps[-1])
        if result: 
            self.tags.append(result)
            self.steps[-1] = self.steps[-1].replace('1-0', '').replace('0-1', '')
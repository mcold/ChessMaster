# coding: utf-8
import xml.etree.ElementTree as ET
from pathlib import Path
from db import Gingko
import re

file_gingko = 'Chess.md'

def get_gingko_tree(file: str) -> Gingko:
    parser = ET.XMLParser(encoding='utf-8')
    tree = ET.parse(file, parser=parser)
    root = tree.getroot()
    g = Gingko(root.attrib['id'], root.text.strip())
    g.childs = [get_gingko_child(gingko_xml = gi) for gi in root]
    g.id = g.id.rpartition('-')[-1] # only for root
    return g

def get_gingko_child(gingko_xml: ET.Element) -> Gingko:
    # TODO: get tags - differ block line and tag-line
    g = Gingko(gingko_xml.attrib['id'], gingko_xml.text.strip())
    g.childs = [get_gingko_child(gingko_xml = gci) for gci in gingko_xml]
    return g

def get_result(s: str) -> str:
    if s.find('1-0'): return '1-0'
    if s.find('1-0'): return '0-1'
    return None


def load_game(s: str) -> None:
    g_ext = Gingko(block=s)
    g_int = get_gingko_tree(file = file_gingko)
    if g_ext != g_int:
        if g_int.steps[0] == g_ext.steps[0]:
            g_int += g_ext
        else:
            g_int.childs.append(g_ext)
    g_int.gen_ids()
    # TODO: Write to file


def get_branch(block: str) -> Gingko:
    """
    Get gingko with current steps subsequence
    """

def get_tasks() -> list:
    """
    Get list of tasks
    Define by tag
    """

def get_game_by_id(id: int) -> Gingko:
    """
    Get game by id
    """


if __name__ == "__main__":
    g = get_gingko_tree(file = file_gingko)
    print(g.__repr__())
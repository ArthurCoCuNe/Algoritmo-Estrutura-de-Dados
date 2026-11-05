import sys
from pathlib import Path

# Sobe 2 pastas a partir de pospreinfixa.py para chegar em "D:\UFRJ\Algoritmo e Estrutura de Dados"
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import EstruturasDeDados.Data_Structures.Trees.Binary_Search_Trees.Binary_Search_Tree.binary_search_tree as tree

def BuscarArvore(arvore: tree, valor: int) -> bool:
    if arvore.root is None:
        return False

    if arvore.node.left != None:
        BuscarArvore(arvore.node.left, valor)

    if arvore.node.right != None:
        BuscarArvore(arvore.node.right, valor)

    if arvore.node.val == valor:
        return True
    return False

import unittest
import os
import sys
print("Iniciando teste...")
print(f"Diretório atual: {os.getcwd()}")

class TestSimples(unittest.TestCase):
    def test_exemplo(self):
        print("Executando teste exemplo")
        self.assertTrue(True)

if __name__ == '__main__':
    print("Executando testes...")
    unittest.main(verbosity=2) 
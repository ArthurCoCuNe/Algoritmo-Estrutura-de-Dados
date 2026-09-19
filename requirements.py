import sys
import importlib.metadata
import subprocess

def check_environment():
    print("="*50)
    print(" VERIFICADOR DE AMBIENTE - TORRE DE HANÓI 3D")
    print("="*50)
    
    # 1. Validação do Python
    py_version = sys.version_info
    print(f"[+] Python detectado: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
        print("[-] AVISO: Recomenda-se Python 3.8 ou superior para melhor estabilidade.")
        
    # 2. Validação do VPython
    try:
        vpython_version = importlib.metadata.version('vpython')
        print(f"[+] VPython instalado: versão {vpython_version}")
    except importlib.metadata.PackageNotFoundError:
        print("[-] ERRO FATAL: Biblioteca 'vpython' não encontrada.")
        print("\nPara instalar, execute o comando abaixo no terminal:")
        print("    python -m pip install vpython")
        sys.exit(1)
        
    # 3. Validação do Setuptools (Crucial para o erro de pkg_resources no VPython)
    try:
        setuptools_version = importlib.metadata.version('setuptools')
        print(f"[+] Setuptools instalado: versão {setuptools_version}")
        
        # Checa se a versão do setuptools é 70 ou superior
        v_major = int(setuptools_version.split('.')[0])
        if v_major >= 70:
            print("\n[!] ALERTA DE COMPATIBILIDADE [!]")
            print("A versão do setuptools é >= 70. O VPython pode falhar ao buscar o 'pkg_resources'.")
            print("Se o simulador travar na importação, faça o downgrade executando:")
            print("    python -m pip install \"setuptools<70\"")
    except importlib.metadata.PackageNotFoundError:
        print("[-] ERRO: 'setuptools' não encontrado. Necessário para o vpython.")
        print("    Execute: python -m pip install setuptools")

    print("="*50)
    print("Verificação concluída. Você pode executar o arquivo principal da simulação.")

if __name__ == '__main__':
    check_environment()
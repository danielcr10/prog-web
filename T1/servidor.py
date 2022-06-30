from sys import stderr
from socket import getaddrinfo, socket
from socket import AF_INET, SOCK_STREAM
from posix import abort
from os import fork, path
from config import ARQSDEFAULT, PORTA, DIRFISICO, PAGERRO
from datetime import datetime
from time import sleep


# Valida se o arquivo solicitado está dentro das suportadas pelo servidor
def validaExtensaoArq(arq):
    extensao = arq.split('.')[1]
    if extensao not in ['html', 'js', 'jpeg', 'jpg', 'png', 'gif']:
        return False
    return True

def validaConfig():
    # Valida o dirtorio local
    if not path.isdir(DIRFISICO):
        print("Diretório local inválido.", file=stderr)
        exit()
    
    # Valida a página de erro
    try:
        teste = open(DIRFISICO+'/'+PAGERRO, mode="rb").read()
    except:
        print("Pagina de erro não encontrada.", file=stderr)
        exit()
    
    try:
        if not validaExtensaoArq(DIRFISICO+'/'+PAGERRO):
            print("Extensão do arquivo de erro inválido.", file=stderr)
            exit()
    except:
        print("Extensão do arquivo de erro inválido.", file=stderr)
        exit()


    # Valida a porta
    if not isinstance(PORTA, int):
        print("Porta inválida.", file=stderr)
        exit()

    # Valida os arquivos default
    for arquivo in ARQSDEFAULT:
        if not validaExtensaoArq(arquivo):
            print(F"Extensão do arquivo default {arquivo} inválido.", file=stderr)
            exit()

    return

# Tratamento do content-type dependendo do arquivo retornado
def pegaTipoArq(caminho):
    ext = caminho.split('.')[1]
    if ext.upper() == 'HTML' or ext.upper() == 'JS':
        if ext.upper() == 'JS':
            tipo = 'text/javascript'
        else:
            if ext.lower() == 'jpg':
                ext = 'jpeg'
            tipo = 'text/'+ext.lower()
    else:
        tipo = 'image/'+ext.lower()
    return tipo

def trataRequisicao(msg):
    req = msg.splitlines()[0]
    metodo, diretorio, prot = req.split(' ')
    # Avalia o metodo da requisicao
    if metodo.upper() == 'GET':
        # avalia se eh solicitado um arquivo
        if '.' not in diretorio:
            # Tenta abrir a lista de arquivos
            count = 0
            # Passa por todos os arquivos da lista default na ordem, ao encontrar o primeiro válido retorna como resposta
            for pagina in ARQSDEFAULT:
                try:
                    arqRet = open(DIRFISICO+'/'+pagina, mode="rb").read()
                    codHttp = 200
                    msgRet = ''
                    msgRet += "HTTP/1.1 " + str(codHttp)
                    descCodHttp = ' OK\r\n'
                    msgRet += descCodHttp
                    msgRet += "Server: Apache-Coyote/1.1\r\n"
                    tipoArquivo = pegaTipoArq(pagina)
                    msgRet += "Content-Type: " + tipoArquivo + "\r\n"
                    msgRet += "Content-Length: " + str(len(arqRet)) + "\r\n"
                    msgRet += "Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S") +" GMT\r\n"
                    msgRet += "\r\n"
                    return [msgRet, arqRet]
                # Caso não encontre nenhum válido na lista prepara a pagina de erro 404 e envia ao finalizar a lista
                except:
                    if count == 0:
                        codHttp = 404
                        arqRet = open(DIRFISICO+'/'+PAGERRO, mode="rb").read()
                        msgRet = ''
                        msgRet += "HTTP/1.1 " + str(codHttp)
                        descCodHttp = ' Erro\r\n'
                        msgRet += descCodHttp
                        msgRet += "Server: Apache-Coyote/1.1\r\n"
                        tipoArquivo = pegaTipoArq(PAGERRO)
                        msgRet += "Content-Type: " + tipoArquivo + "\r\n"
                        msgRet += "Content-Length: " + str(len(arqRet)) + "\r\n"
                        msgRet += "Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S") +" GMT\r\n"
                        msgRet += "\r\n"
                    count += 1
            return [msgRet, arqRet]
        
        # Solicita um arquivo diretamente
        else:
            # Valida a extensao do arquivo solicitado
            if validaExtensaoArq(diretorio):
                # Tenta abrir o arquivo
                try:
                    arqRet = open(DIRFISICO+diretorio, mode="rb").read()
                    codHttp = 200
                # Caso não exista no diretório retorna um erro 404
                except:
                    print("Arquivo nao encontrado:", DIRFISICO+diretorio, file=stderr)
                    codHttp = 404
                    arqRet = open(DIRFISICO+'/'+PAGERRO, mode="rb").read()
                msgRet = ''
                msgRet += "HTTP/1.1 " + str(codHttp)
                if codHttp == 200:
                    descCodHttp = ' OK\r\n'
                else:
                    descCodHttp = ' Erro\r\n'
                msgRet += descCodHttp
                msgRet += "Server: Apache-Coyote/1.1\r\n"
                tipoArquivo = pegaTipoArq(diretorio)
                msgRet += "Content-Type: " + tipoArquivo + "\r\n"
                msgRet += "Content-Length: " + str(len(arqRet)) + "\r\n"
                msgRet += "Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S") +" GMT\r\n"
                msgRet += "\r\n"
                return [msgRet, arqRet]
            else:
                print("Tipo de arquivo nao suportado", file=stderr)
    return

# Colocando o server de pé
def main():
    # Validando dados do arquivo de configuração
    validaConfig()
    # Setup inicial
    host = ''
    bufferSize = 1024
    porta = PORTA
    if not PORTA:
        porta = 8080

    # Criando o socket
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    if not tcpSocket:
        print("Não consegui criar o socket", file=stderr)
        abort()
    origem = (host, porta)

    # Fazendo bind no socket
    try:
        tcpSocket.bind(origem)
    except:
        print("Erro ao dar bind no socket do servidor", porta, file=stderr)
        abort()

    # Escutar a porta definida
    try:
        tcpSocket.listen(0)
    except:
        print("Erro ao começar a escutar a porta", file=stderr)
        abort()

    print(f"Servidor pronto no endereço http://localhost:{porta}")

    # Server disponivel para receber solicitações com conexões simultaneas
    while True:
        # Estabelecendo conexao
        con, cliente = tcpSocket.accept()
        pid = fork()
        if pid == 0:
            tcpSocket.close()
            print("Servidor conectado com ", cliente)
            while True:
                msg = con.recv(bufferSize).decode("utf-8")
                if not msg:
                    break
                # Tratando a solicitação
                msgRet, arqRet = trataRequisicao(msg)
                # Envia a resposta para o solicitante
                con.send(bytearray(msgRet, 'utf-8'))
                con.send(arqRet)
            print("Conexao finalizada")
            con.close()
            exit()
        else:
            con.close()
    return


if __name__ == '__main__':
    main()

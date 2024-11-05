# Simulação de Tabelas de Roteamento e Envio de Mensagens entre Roteadores

Este projeto simula uma rede de roteadores, onde cada roteador possui uma tabela de roteamento que é atualizada periodicamente com base em informações trocadas entre vizinhos. A aplicação permite também o envio de mensagens de texto entre roteadores, com encaminhamento conforme as rotas definidas nas tabelas.

## Requisitos

- **Python 3.8+**
- **Bibliotecas padrão do Python**, como `socket`, `time`, e `logging`.
  
### Configuração do Arquivo `routers.txt`

Cada roteador precisa de um arquivo `routers.txt` onde são especificados os endereços IP e portas dos roteadores vizinhos. Cada linha do arquivo deve conter um endereço IP e um número de porta no formato `localhost:porta` ou `IP:porta`.

### Estrutura do Projeto

- `router.py`: Código principal que inicia e executa o roteador.
- `routing_table.py`: Gerencia a tabela de roteamento, incluindo adição, atualização e remoção de rotas.
- `routers.txt`: Arquivo de configuração que define os roteadores vizinhos.

## Como Executar Localmente

### Passo a Passo para Simular Múltiplos Roteadores em uma Máquina Local

1. **Configurar o `routers.txt`**:
   - Para cada roteador, crie uma cópia do arquivo `routers.txt` com uma lista de vizinhos específica para a topologia desejada. Exemplo de configuração para um roteador:
     ```
     localhost:9002
     localhost:9003
     ```

2. **Iniciar Instâncias do Roteador**:
   - Em terminais separados, execute o `router.py` com o IP `localhost` e a porta específica para cada instância. Por exemplo:
     ```bash
     python router.py localhost 9001
     python router.py localhost 9002
     python router.py localhost 9003
     python router.py localhost 9004
     ```

   Cada instância irá usar o arquivo `routers.txt` correspondente para se conectar com seus vizinhos.

3. **Testar Atualizações de Tabela de Roteamento**:
   - Observe que as tabelas de roteamento serão trocadas automaticamente a cada 15 segundos. No terminal, você verá as atualizações conforme novas rotas são descobertas ou removidas.

4. **Enviar Mensagens de Texto**:
   - Para testar o envio de mensagens entre roteadores, você pode enviar mensagens manualmente informando o IP de origem, destino e o conteúdo da mensagem. O formato de mensagem é `!IP_origem;IP_destino;Mensagem`. O roteador irá encaminhar a mensagem automaticamente até o destino.

### Observando o Funcionamento

Os logs no terminal mostrarão cada mensagem recebida e qualquer atualização na tabela de roteamento, permitindo que você acompanhe a comunicação entre os roteadores.

---

## Como Executar em Rede (Modo Online)

### Pré-requisitos para Execução em Rede

Para rodar a aplicação em máquinas diferentes em uma rede, você precisará definir IPs reais em `routers.txt` e garantir que cada máquina tenha conectividade na rede local ou pela internet.

1. **Configurar o Arquivo `routers.txt`**:
   - Em cada máquina, crie o arquivo `routers.txt` com os IPs e portas dos roteadores vizinhos na rede. Por exemplo:
     ```
     192.168.1.2:9000
     192.168.1.3:9000
     ```
   - Certifique-se de que o IP da máquina corresponde ao endereço listado no arquivo de configuração de seus vizinhos.

2. **Liberar a Porta no Firewall**:
   - Certifique-se de que a porta 9000 esteja liberada no firewall de cada máquina para permitir a comunicação via UDP.

3. **Iniciar o Roteador em Cada Máquina**:
   - Em cada máquina, execute o seguinte comando no terminal:
     ```bash
     python router.py <IP_da_máquina> 9000
     ```
   - Substitua `<IP_da_máquina>` pelo IP real da máquina onde o roteador está sendo executado.

4. **Teste de Envio de Mensagens**:
   - Envie mensagens de um roteador para outro especificando o IP e o texto da mensagem. Cada roteador exibirá a mensagem no terminal, indicando se foi recebida, encaminhada ou se chegou ao destino final.

### Exemplo de Execução de Mensagens de Teste

Para enviar uma mensagem de um roteador para outro, insira o seguinte comando no console do roteador:
```python
router.send_message("!", "<IP_origem>;<IP_destino>;<Sua mensagem>")
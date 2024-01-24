Esse projeto foi utilizado para resolver o seguinte problema dentro da empresa que eu trabalho:
- Trabalho em uma empresa de software de automação comercial. Atendemos diversos clientes, como padarias, restaurantes e afins. Mensalmente, cada um desses clientes precisa enviar para a sua respectiva contabilidade um email com todos os arquivos fiscais emitidos pela empresa, arquivos estes que ficam salvos no computador local de cada caixa.
- Até há uma ferramenta dentro do próprio software aqui da empresa em que o cliente consegue fazer esse envio para a contabilidade dele, mas isso precisa ser feito manualmente pelo cliente ou por algum responsável designado pelo dono do estabelecimento para fazer isso todos os meses. Portanto foi levntado a questão se havia alguma forma desse envio ser feito automaticamente.
- Portanto desenvolvi essa aplicação em python que, programado junto ao agendador de tarefas do windows, uma vez por mês, realiza o envio dos arquivos para um email pré cadastrado no arquivo de configuração "config.ini".

Essa aplicação possui uma utilização bem específica aqui na empresa, pois todos os arquivos ficam salvos numa pasta específica no disco local "c:", e todo mês o nome dessa pasta muda, sempre seguindo o padrão "ano/mes", por exemplo "202312" ou "202401". Portanto o local de onde esses arquivos serão extraídos é sempre o mesmo, a única informação que muda é a pasta, portanto, o local foi definido no próprio código da seguinte maneira: 
- "C:/Pacnet/pdv/Vendas". "C:" basicamente é o armazenamento padrão do windows, "Pacnet" é onde os arquivos do sistema são gravados, "vendas" é a pasta onde os arquivos fiscais são armazenados. A partir daí há mais duas pastas, a primeira é o CNPJ da empresa cliente, que deve ser definido no arquvio de configuração "config.ini" no campo CNPJ. E a pasta do mês dos arquivos é definida automaticamente por meio de uma função no código do python, sempre pegando a pasta do mês anterior ao qual estamos agora, portanto se você está lendo isso no dia 15 de Janeiro de 2024, a pasta selecionada seria 202312, que é a pasta do mês passado.

Sobre o arquivo de configuração:
- Existem 3 configuração a ser feita no arquivo "config.ini":
  - A primeira delas é o CNPJ cliente, conforme explicado acima.
  - A segunda delas é o email da contabilidade, para onde o email da aplciação será enviado, contendo os arquivos fiscais.
  - A terceira delas é o perfil, nesse caso se refere ao perfil do caixa. Como os arquivos são enviados caixa à caixa então é necessário definir o perfil para que isso conste no email enviado.

As outras informações, como o email fonte, ou seja, de onde será enviado o email, o corpo do email e afins está definido diretamente no código fonte da aplicação, no "sript.py". Visto que essa aplicação seria uma aplicação para ficar parada e executando mensalmente, portanto essa foi a razão de definir isso no código fonte da aplicação e o que fosse "modificável" ser definido via arquivo de configuração.

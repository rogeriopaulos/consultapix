# Consulta Pix

Aplicação para consulta de dados do Pix de indivíduos perante o Bacen.

[![Construído com Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Licença: MIT

## Configurações

Movido para [configurações](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Comandos Básicos

### Configurando Seus Usuários

- Para criar uma **conta de usuário normal**, basta acessar a página de cadastro e preencher o formulário. Após enviar, você verá uma página "Verifique Seu Endereço de E-mail". Vá até o console para ver uma mensagem simulada de verificação de e-mail. Copie o link no seu navegador. Agora o e-mail do usuário deve estar verificado e pronto para uso.

- Para criar uma **conta de superusuário**, use este comando:

      $ python manage.py createsuperuser

Para conveniência, você pode manter seu usuário normal logado no Chrome e seu superusuário logado no Firefox (ou similar), para que você possa ver como o site se comporta para ambos os tipos de usuários.

### Verificação de Tipos

Executando verificações de tipos com mypy:

    $ mypy consultapix

### Cobertura de Testes

Para executar os testes, verificar a cobertura de testes e gerar um relatório de cobertura em HTML:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Executando testes com pytest

    $ pytest

### Celery

Este aplicativo vem com o Celery.

Para executar um worker do Celery:

```bash
cd consultapix
celery -A config.celery_app worker -l info
```

Por favor, note: Para que a mágica de importação do Celery funcione, é importante _onde_ os comandos do Celery são executados. Se você estiver na mesma pasta que o _manage.py_, você deve estar no lugar certo.

Para executar [tarefas periódicas](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), você precisará iniciar o serviço de agendador do Celery Beat. Você pode iniciá-lo como um processo independente:

```bash
cd consultapix
celery -A config.celery_app beat
```

ou você pode embutir o serviço beat dentro de um worker com a opção `-B` (não recomendado para uso em produção):

```bash
cd consultapix
celery -A config.celery_app worker -B -l info
```

### Servidor de E-mail

No desenvolvimento, é frequentemente útil poder ver os e-mails que estão sendo enviados pelo seu aplicativo. Por essa razão, o servidor SMTP local [Mailpit](https://github.com/axllent/mailpit) com uma interface web está disponível como um contêiner Docker.

O contêiner mailpit será iniciado automaticamente quando você executar todos os contêineres Docker.
Por favor, verifique a [documentação Docker do cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html) para mais detalhes sobre como iniciar todos os contêineres.

Com o Mailpit em execução, para visualizar as mensagens enviadas pelo seu aplicativo, abra seu navegador e acesse `http://127.0.0.1:8025`.

### Sentry

O Sentry é um serviço agregador de registro de erros. Você pode se inscrever para uma conta gratuita em <https://sentry.io/signup/?code=cookiecutter> ou baixá-lo e hospedá-lo você mesmo.
O sistema está configurado com padrões razoáveis, incluindo registro de erros 404 e integração com o aplicativo WSGI.

Você deve configurar a URL DSN em produção.

## Implantação

Os detalhes a seguir explicam como implantar este aplicativo.

### Docker

Veja a [documentação Docker do cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html) para mais detalhes.

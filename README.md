# King Pong (Transcendence)
![Version](https://img.shields.io/badge/version-0.0.0-blue)
![GitHub Issues](https://img.shields.io/github/issues/vitorsantanna2/transcendence.svg)
![Live Demo](https://img.shields.io/badge/status-offline-red.svg)


Este projeto consiste em um jogo de Ping Pong multiplayer, e foi criado com a finalidade de finalizar o currículo básico(common-core) da 42Rio.

## Referência

 - [Django Documentation](https://docs.djangoproject.com/en/5.0/)
 - [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
 - [Psycopg3 Documentation](https://www.psycopg.org/psycopg3/docs/index.html)
 - [Postgresql Documentation](https://www.postgresql.org/docs/)


## Autores

- [@vitorsantanna2](https://github.com/vitorsantanna2)
- [@psydenst](https://github.com/psydenst)
- [@VictorVasconcellos42](https://github.com/VictorVasconcellos42/)
- [@amenesca](https://github.com/amenesca)
- [@nands93](https://github.com/nands93)



## Rodando localmente

Instale os requisitos da aplicação e execute o servidor:

Instale o poetry para o versionamento:
```bash
  make setup
```
Crie um arquivo dentro da pasta local com o nome de settings.dev.py para armazenar as variáveis de ambiente.
Existe um template aqui do [arquivo](https://github.com/vitorsantanna2/transcendence/blob/main/core/kingkong/settings/templates/settings.dev.py)

Execute o programa:
```bash
    make run
```

## Contribuindo

Instale o pre-commit (faz com que o código seja corrigido dentro da norma antes de ser commitado):
```bash
   make install-pre-commit
```

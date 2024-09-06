FROM python:3.10.12-alpine

# Adiciona um usuário para rodar o Gunicorn

# Cria o diretório de trabalho
RUN mkdir /code
WORKDIR /code

# Copia o código da aplicação para o container
COPY ../../ /code/

# Instala as dependências necessárias
RUN apk add --no-cache \
    python3-dev \
    build-base \
    linux-headers \
    pcre-dev \
    libpq-dev \
    sdl2-dev \
    sdl2_image-dev \
    sdl2_mixer-dev \
    sdl2_ttf-dev \
    freetype-dev \
    pkgconfig

# Instala as dependências do Python
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
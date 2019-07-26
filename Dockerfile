FROM centos:7

RUN yum update -y
RUN yum install -y bzip2 bzip2-devel gcc gcc-c++ make openssl-devel readline-devel zlib-devel wget curl unzip vim epel-release git && \
    yum install -y tig jq vim-enhanced bash-completion net-tools bind-utils libffi-devel chrpath && \
    rm -rf /var/cache/yum/*

RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LC_CTYPE "ja_JP.UTF-8"
ENV LC_NUMERIC "ja_JP.UTF-8"
ENV LC_TIME "ja_JP.UTF-8"
ENV LC_COLLATE "ja_JP.UTF-8"
ENV LC_MONETARY "ja_JP.UTF-8"
ENV LC_MESSAGES "ja_JP.UTF-8"
ENV LC_PAPER "ja_JP.UTF-8"
ENV LC_NAME "ja_JP.UTF-8"
ENV LC_ADDRESS "ja_JP.UTF-8"
ENV LC_TELEPHONE "ja_JP.UTF-8"
ENV LC_MEASUREMENT "ja_JP.UTF-8"
ENV LC_IDENTIFICATION "ja_JP.UTF-8"
ENV LC_ALL ja_JP.UTF-8

ENV PYTHON_CONFIGURE_OPTS "--enable-shared"
ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH

WORKDIR /app
RUN curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
RUN export PATH="~/.pyenv/bin:$PATH" && \
    echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

RUN eval "$(pyenv init -)" && \
    eval "$(pyenv virtualenv-init -)" && \
    pyenv install 3.7.3 && \
    pyenv global 3.7.3 && \
    pip install --upgrade pip

RUN eval "$(pyenv init -)" && \
    eval "$(pyenv virtualenv-init -)" && \
    pip install --no-cache-dir "poetry==0.12.17"

COPY pyproject.toml poetry.lock README.md LICENSE ./
COPY zabbix_controller ./zabbix_controller

RUN eval "$(pyenv init -)" && \
    eval "$(pyenv virtualenv-init -)" && \
    poetry config settings.virtualenvs.create true && \
    poetry config settings.virtualenvs.in-project true && \
    poetry install --no-interaction


RUN eval "$(pyenv init -)" && \
    eval "$(pyenv virtualenv-init -)" && \
    poetry run pyinstaller \
    --onefile \
    zabbix_controller/call_command.py

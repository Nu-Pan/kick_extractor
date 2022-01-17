
# Install ubuntu latest
FROM ubuntu:focal

# Install deb packages
RUN perl -p -i.bak -e 's%(deb(?:-src|)\s+)https?://(?!archive\.canonical\.com|security\.ubuntu\.com)[^\s]+%$1http://ftp.tsukuba.wide.ad.jp/Linux/ubuntu/%' /etc/apt/sources.list \
&&  export DEBIAN_FRONTEND=noninteractive \
&&  apt-get update \
&&  apt-get -y install --no-install-recommends \
    python3 pip gosu \
&&  apt-get autoremove -y \
&&  apt-get clean \
&&  rm -rf /user/local/src/*

# Install pip packages
RUN pip install -U pip \
&&  pip install --no-cache-dir numpy scipy jupyterlab bokeh sympy

# User settings
ENV USER_NAME=dev \
    GROUP_ID=1000 \
    USER_ID=1000
RUN groupadd -g $GROUP_ID $USER_NAME \
&&  useradd -d /home/$USER_NAME -m -s /bin/bash -u $USER_ID -g $GROUP_ID $USER_NAME \
&&  echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Launch settings
COPY    entrypoint.sh /usr/local/bin/entrypoint.sh
RUN     chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

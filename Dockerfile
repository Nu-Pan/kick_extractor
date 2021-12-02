
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
&&  pip install --no-cache-dir numpy scipy jupyterlab bokeh

# Launch settings
COPY    entrypoint.sh /user/local/bin/entrypoint.sh
RUN     chmod +x /user/local/bin/entrypoint.sh
ENTRYPOINT ["/user/local/bin/entrypoint.sh"]

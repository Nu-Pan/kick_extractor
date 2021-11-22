
# Install ubuntu latest
FROM ubuntu:focal

# Install deb packages
RUN perl -p -i.bak -e 's%(deb(?:-src|)\s+)https?://(?!archive\.canonical\.com|security\.ubuntu\.com)[^\s]+%$1http://ftp.tsukuba.wide.ad.jp/Linux/ubuntu/%' /etc/apt/sources.list \
&&  export DEBIAN_FRONTEND=noninteractive \
&&  apt-get update \
&&  apt-get -y install --no-install-recommends \
    python3 pip \
&&  apt-get autoremove -y \
&&  apt-get clean

# Install pip packages
RUN pip install scipy jupyterlab matplotlib lmfit

# Launch settings
VOLUME  /kick_extractor
WORKDIR /kick_extractor
ENV     PWD=/kick_extractor
ENV     JUPYTER_ENABLE_LAB=true
EXPOSE  8888/tcp
CMD     ["jupyter-lab", "--ip", "0.0.0.0", "--allow-root"]

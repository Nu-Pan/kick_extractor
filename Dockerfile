
# Install ubuntu latest
FROM ubuntu

# Install deb packages
RUN export DEBIAN_FRONTEND=noninteractive \
&&  apt-get update \
&&  apt-get -y install --no-install-recommends python3 pip git

# Install pip packages
RUN pip install scipy

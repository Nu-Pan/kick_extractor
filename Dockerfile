
# Install ubuntu latest
FROM ubuntu

# Install deb packages
RUN apt-get update \
&&  export DEBIAN_FRONTEND=noninteractive \
&&  apt-get -y install --no-install-recommends python3 pip git

# Install pip packages
RUN pip install scipy

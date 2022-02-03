# Creator:   VPR
# Created:   February 3, 2022
# Updated:   February 3, 2022

set -e pipefail
set -e errexit
set -e nounset
set -e xtrace

# Install open-ssl if not already installed
if [ $(dpkg-query -W -f='${Status}' openssl 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt-get install openssl;
fi

# House certificates in home directory
mkdir -p ~/certs
cd ~/certs

# Generate private key
openssl genrsa -des3 -out local-CA.key 4096

# Generate root certificate
openssl req -x509 -new -nodes -key local-CA.key -sha256 -days 365 -out root-CA.pem
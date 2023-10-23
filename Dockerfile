FROM ubuntu:22.04

ARG VERSION

RUN apt update && apt install -y wget unzip
RUN wget https://certificates.trustedservices.intel.com/Intel_SGX_Attestation_RootCA.pem
RUN wget https://github.com/acompany-develop/SGX-EIM-DEMO/releases/download/${VERSION}/SGX-EIM-v${VERSION}-linux-x64.zip
RUN unzip SGX-EIM-v${VERSION}-linux-x64.zip


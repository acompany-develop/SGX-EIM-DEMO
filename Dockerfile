FROM ubuntu:22.04
RUN apt update && apt install -y wget
RUN wget https://certificates.trustedservices.intel.com/Intel_SGX_Attestation_RootCA.pem
COPY cross_app_bin .
COPY match_app_bin .

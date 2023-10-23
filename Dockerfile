FROM ubuntu:22.04
RUN apt update && apt install -y wget
RUN wget https://certificates.trustedservices.intel.com/Intel_SGX_Attestation_RootCA.pem

ARG VERSION="v0.1.1"
COPY binary/${VERSION}/cross_app_bin .
COPY binary/${VERSION}/match_app_bin .

#
# SPDX-FileCopyrightText: Copyright 2022 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT
#
FROM ghcr.io/jishminor/server/tritonserver:2.15.0_armnn_v21.08_ruy_on_gpu_off_backendver_v0.2.0_release
ADD . .
RUN chmod +x invoke_server.sh
CMD ./invoke_server.sh

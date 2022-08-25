#
# SPDX-FileCopyrightText: Copyright 2022 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT
#

ids=$(docker ps -a -q)
for id in $ids
do
 echo "$id"
 docker stop $id && docker rm $id
done

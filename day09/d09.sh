#!/usr/bin/env bash
echo -n "Part 1: "
echo -e "$(cat d09.in)\n1" | python3 ../day05/d05-intCode.py
echo -n "Part 2: "
echo -e "$(cat d09.in)\n2" | python3 ../day05/d05-intCode.py
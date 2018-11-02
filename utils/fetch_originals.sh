#!/bin/bash

source_url="https://urlausnir.stuff.is/skrar/Haestirettur/bindi/"

wget --recursive --no-parent -e robots=off -R "index.html*" -nd -A pdf,txt -P ../pdf/originals -nc $source_url
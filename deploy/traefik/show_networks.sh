#!/bin/bash

docker inspect  --format='{{ .Name }} {{ println }}{{ range $n, $conf := .NetworkSettings.Networks }}  {{ $n }} : {{ $conf.IPAddress }} {{ println }}{{ end }}  Ports: {{range $p, $conf := .NetworkSettings.Ports }} {{ if $conf }} {{ (index $conf 0).HostIp }}:{{ (index $conf 0).HostPort }} -> {{ $p }} {{ else }} {{ $p }} {{ end }} {{ end }}' $(docker ps --format '{{ .ID }}')


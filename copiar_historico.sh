#!/bin/bash

CONTAINER=$(docker ps --filter "name=servidor" --format "{{.Names}}")
if [ -z "$CONTAINER" ]; then
  echo "Servidor não está rodando!"
else
  docker cp $CONTAINER:/historico ./
  echo "Histórico copiado para ./historico"
fi

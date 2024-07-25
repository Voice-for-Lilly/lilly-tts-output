#!/bin/bash
screen -dmS tts bash -c 'tts-server --model_name tts_models/de/thorsten/vits --use_cuda true'
python3 lilly-tts-api.py
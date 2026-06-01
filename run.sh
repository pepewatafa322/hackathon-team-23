#!/bin/bash
pip install -r requirements.txt
python3 -m src.main --inbox inbox --output processed || python -m src.main --inbox inbox --output processed

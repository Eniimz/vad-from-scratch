# vad-from-scratch

Voice activity detection from scratch. No libraries that hide the pipeline — just framing, then energy and ZCR.

```
vad-from-scratch/
├── vad/
│   ├── __init__.py
│   ├── framing.py
│   ├── features.py
│   └── plotting.py
├── tests/
│   ├── test_audio.wav
│   └── transfer_test_audio.wav
└── requirements.txt
```

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python vad/framing.py
```

# FakeLens — Image Forgery Localization

**Author:** Nikita Nizov

FakeLens is a deep learning system for pixel-level localization of image manipulations using DINOv3, LoRA, and a convolutional segmentation decoder.

### Live Demo

[Try FakeLens on Hugging Face](https://huggingface.co/spaces/T1-Reks/fakelens)

### Model Weights

The trained model checkpoint is available on Hugging Face:

[Download FakeLens checkpoint](https://huggingface.co/spaces/T1-Reks/fakelens/blob/main/forgerylens_compact_best.pt)

The checkpoint contains the fine-tuned LoRA adapters and convolutional segmentation decoder (~27.6 MiB).

The pretrained DINOv3 backbone is not included and must be loaded separately.

### Source Code

- [Training and evaluation](FakeLens.ipynb)
- [Gradio application](https://huggingface.co/spaces/T1-Reks/fakelens/tree/main)

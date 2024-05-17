# E2M (Everything to Markdown)

<p align="center">
    <a href="https://github.com/Jing-yilin/E2M">
        <img src="https://img.shields.io/badge/E2M-repo-blue" alt="E2M Repo">
    </a>
</p>

- [E2M (Everything to Markdown)](#e2m-everything-to-markdown)
  - [Introduction](#introduction)
  - [Install](#install)
  - [Get Started](#get-started)
    - [Quick Start](#quick-start)
    - [Set to Development Environment](#set-to-development-environment)
    - [Set to Production Environment](#set-to-production-environment)
  - [How to contribute](#how-to-contribute)
    - [PEP8 style](#pep8-style)
  - [Supported File Types](#supported-file-types)
  - [Support](#support)
  - [Join Us](#join-us)

## Introduction

This project aims to provide an API, which can convert everything to markdown (LLM-friendly Format).

## Install

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M
conda create -n e2m python=3.10
conda activate e2m
python -m pip install -r requirements.txt
```

## Get Started

### Quick Start

```bash
# make sure you are in E2M/app
cd app
flask run --host 0.0.0.0 --port=8765
```

### Set to Development Environment

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Set to Production Environment

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

## How to contribute

### PEP8 style

```bash
# all contributions should follow PEP8 style
flake8 .  # to check the style
black .  # to format the code
```

## Supported File Types

## Support

## Join Us

+++
date = '2026-03-15T10:00:00+09:00'
draft = false
title = 'Docker 기초 가이드'
categories = ['DevOps']
tags = ['docker', 'container', 'devops']
description = 'Docker 컨테이너의 기초부터 실전까지 알아봅니다.'
+++

## Docker란?

Docker는 애플리케이션을 컨테이너로 패키징하여 어디서든 실행할 수 있게 해주는 플랫폼입니다.

### 기본 명령어
```bash
docker build -t myapp .
docker run -p 8080:8080 myapp
```

# [2021년] DevOps 프로젝트 기반 클라우드 교육 준비

## docker-compose

본 프로젝트는 도커 컴포즈를 통해 서비스를 한 번에 구동할 수 있습니다.

```
docker-compose up -d  # detach 모드로 서비스 구동
docker-compose ps     # 서비스 프로세스 확인
```

## 구동되는 서비스

* web django : http://localhost:8000
* mysql : 포트 3306
* memcache : 포트 11211
* redis : 포트 6379
* web phpmyadmin : http://localhost:8080

## 강사

Ask Company 이진석

- me@askcompany.kr
- http://facebook.com/groups/askdjango
- 인프런 "[파이썬/장고 웹서비스 개발 완벽 가이드 with 리액트](https://www.inflearn.com/course/파이썬-장고-웹서비스?inst=6a0dda6d)"

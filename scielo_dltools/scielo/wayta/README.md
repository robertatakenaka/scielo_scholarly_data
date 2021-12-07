# WAYTA

Criada para atender a padronização de nomes de instituições encontradas em afiliações.

Tinha a intenção de fazer correções automatizadas, como por exemplo, transformar "X" (identificação incorreta da afiliação dentro de um documento específico) em "Universidade de São Paulo".


## Uso da API

http://es.scielo.org:9200/wayta_institutions/_search?from=2&size=5

* from: identifica a página
* size: indica quantos items por página

```json

{

    "took": 28,
    "timed_out": false,
    "_shards": {
        "total": 5,
        "successful": 5,
        "failed": 0
    },
    "hits": {
        "total": 42748,
        "max_score": 1.0,
        "hits": [
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpd-uw9gP5jN5Yquwv",
                "_score": 1.0,
                "_source": {
                    "city": "Acatzingo",
                    "name": "Benemérita Universidad Autónoma de Puebla",
                    "form": "Benemérita Universidad de Puebla",
                    "country": "Mexico",
                    "iso-3166": "MX",
                    "state": "Puebla",
                    "timestamp": "2015-10-27T11:23:59.401439"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpd-vB9gP5jN5Yquwy",
                "_score": 1.0,
                "_source": {
                    "city": "Acatzingo",
                    "name": "Benemérita Universidad Autónoma de Puebla",
                    "form": "EIAH-Benemérita Universidad Autónoma de Puebla",
                    "country": "Mexico",
                    "iso-3166": "MX",
                    "state": "Puebla",
                    "timestamp": "2015-10-27T11:23:59.418213"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpeBsb9gP5jN5YqvOQ",
                "_score": 1.0,
                "_source": {
                    "city": "Waterville",
                    "name": "Colby College",
                    "form": "Colby College",
                    "country": "USA",
                    "iso-3166": "US",
                    "state": "Maine",
                    "timestamp": "2015-10-27T11:24:11.541000"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpeBtO9gP5jN5YqvOa",
                "_score": 1.0,
                "_source": {
                    "city": "Morelia",
                    "name": "Colegio Culinario de Morelia",
                    "form": "Colegio Culinario de Morelia",
                    "country": "Mexico",
                    "iso-3166": "MX",
                    "state": "Michoacán",
                    "timestamp": "2015-10-27T11:24:11.591397"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpeByY9gP5jN5YqvPY",
                "_score": 1.0,
                "_source": {
                    "city": "San Pedro Garza García",
                    "name": "Colegio Labastida",
                    "form": "Colegio Labastida",
                    "country": "Mexico",
                    "iso-3166": "MX",
                    "state": "Nuevo León",
                    "timestamp": "2015-10-27T11:24:11.921746"
                }
            }
        ]
    }

}

```

http://es.scielo.org:9200/wayta_institutions/_search?q=usp&from=2&size=5

* q: expressão de busca
* from: identifica a página
* size: indica quantos items por página

```json

{

    "took": 166,
    "timed_out": false,
    "_shards": {
        "total": 5,
        "successful": 5,
        "failed": 0
    },
    "hits": {
        "total": 237,
        "max_score": 1.638696,
        "hits": [
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpe69d9gP5jN5Yq3Z0",
                "_score": 1.5167013,
                "_source": {
                    "city": "São Paulo",
                    "name": "Universidade de São Paulo",
                    "form": "USP",
                    "country": "Brazil",
                    "iso-3166": "BR",
                    "state": "São Paulo",
                    "timestamp": "2015-10-27T11:28:06.104145"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpe6WS9gP5jN5Yq3Tn",
                "_score": 1.3840458,
                "_source": {
                    "city": "São Paulo",
                    "name": "Universidade de São Paulo",
                    "form": "FCFRP-USP",
                    "country": "Brazil",
                    "iso-3166": "BR",
                    "state": "São Paulo",
                    "timestamp": "2015-10-27T11:28:03.596691"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpe6k99gP5jN5Yq3V5",
                "_score": 1.3840458,
                "_source": {
                    "city": "São Paulo",
                    "name": "Universidade de São Paulo",
                    "form": "Univ de Sao Paulo - USP",
                    "country": "Brazil",
                    "iso-3166": "BR",
                    "state": "São Paulo",
                    "timestamp": "2015-10-27T11:28:04.535803"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpe69X9gP5jN5Yq3Zz",
                "_score": 1.3840458,
                "_source": {
                    "city": "São Paulo",
                    "name": "Universidade de São Paulo",
                    "form": "Univesidade de Sao Paulo - USP",
                    "country": "Brazil",
                    "iso-3166": "BR",
                    "state": "São Paulo",
                    "timestamp": "2015-10-27T11:28:06.098339"
                }
            },
            {
                "_index": "wayta_institutions",
                "_type": "institution",
                "_id": "AVCpe6-z9gP5jN5Yq3aD",
                "_score": 1.3840458,
                "_source": {
                    "city": "São Paulo",
                    "name": "Universidade de São Paulo",
                    "form": "USP -University of Sao Paulo",
                    "country": "Brazil",
                    "iso-3166": "BR",
                    "state": "São Paulo",
                    "timestamp": "2015-10-27T11:28:06.190059"
                }
            }
        ]
    }

}


```
## Referências

https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html
# How to reproduce IOError in file buffer

## Clone this repository

```
git pull https://github.com/yteraoka/fluentd-reproduce-ioerror.git
cd fluentd-reproduce-ioerror
```


## Pull docker images

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.8.1
docker pull fluent/fluentd-kubernetes-daemonset:v1.11.1-debian-elasticsearch7-1.1
```


## Create docker network

```
docker network create fluentd
```


## Run elasticsearch

```
docker run -d --name es --net fluentd --rm \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:7.8.1
```

Wait for started up.

```
curl http://localhost:9200/
```

(Actually, I think there is no relationship between this problem and elasticsearch.)


## Run fluentd

```
docker run -it --name fluentd --net fluentd --rm \
  -e FLUENT_ELASTICSEARCH_HOST=es \
  -e FLUENT_ELASTICSEARCH_PORT=9200 \
  -e FLUENT_ELASTICSEARCH_PATH=/ \
  -e FLUENT_ELASTICSEARCH_BUFFER_FLUSH_INTERVAL=1 \
  -e FLUENT_ELASTICSEARCH_BUFFER_FLUSH_THREAD_COUNT=1 \
  -e FLUENT_ELASTICSEARCH_BUFFER_QUEUE_LIMIT_LENGTH=1000 \
  -v $(pwd)/log:/var/log/containers \
  -v $(pwd)/fluent.conf:/fluentd/etc/fluent.conf \
  fluent/fluentd-kubernetes-daemonset:v1.11.1-debian-elasticsearch7-1.1
```


## Send log on another terminal

```
gzcat log?.gz | ./catlog.py > log/test.log
```

Then following log shows in fluentd log. If not try again.

```
2020-07-28 14:59:19 +0000 [info]: #0 [in_tail_container_logs] following tail of /var/log/containers/test.log
2020-07-28 14:59:21 +0000 [warn]: #0 [out_es] chunk bytes limit exceeds for an emitted event stream: 8650165bytes
2020-07-28 14:59:21 +0000 [warn]: #0 [out_es] chunk bytes limit exceeds for an emitted event stream: 3295317bytes
...
(snip)
...
2020-07-28 14:59:25 +0000 [warn]: #0 [out_es] chunk bytes limit exceeds for an emitted event stream: 7573972bytes
2020-07-28 14:59:26 +0000 [warn]: #0 [out_es] chunk bytes limit exceeds for an emitted event stream: 8169588bytes
2020-07-28 14:59:26 +0000 [warn]: #0 emit transaction failed: error_class=IOError error="closed stream" location="/fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer/file_chunk.rb:82:in `pos'" tag="cafiscode-eks-cluster.default"
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer/file_chunk.rb:82:in `pos'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer/file_chunk.rb:82:in `rollback'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer.rb:339:in `rescue in block in write'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer.rb:332:in `block in write'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer.rb:331:in `each'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer.rb:331:in `write'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/output.rb:1004:in `block in handle_stream_simple'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/output.rb:888:in `write_guard'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/output.rb:1003:in `handle_stream_simple'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/output.rb:878:in `execute_chunking'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/output.rb:808:in `emit_buffered'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/event_router.rb:97:in `emit_stream'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluent-plugin-rewrite-tag-filter-2.2.0/lib/fluent/plugin/out_rewrite_tag_filter.rb:85:in `block in process'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluent-plugin-rewrite-tag-filter-2.2.0/lib/fluent/plugin/out_rewrite_tag_filter.rb:84:in `each'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluent-plugin-rewrite-tag-filter-2.2.0/lib/fluent/plugin/out_rewrite_tag_filter.rb:84:in `process'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/output.rb:797:in `emit_sync'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/event_router.rb:97:in `emit_stream'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:477:in `receive_lines'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:845:in `block in handle_notify'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:877:in `with_io'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:825:in `handle_notify'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:808:in `block in on_notify'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:808:in `synchronize'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:808:in `on_notify'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:653:in `on_notify'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:325:in `block in setup_watcher'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/in_tail.rb:596:in `on_timer'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/cool.io-1.6.0/lib/cool.io/loop.rb:88:in `run_once'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/cool.io-1.6.0/lib/cool.io/loop.rb:88:in `run'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin_helper/event_loop.rb:93:in `block in start'
  2020-07-28 14:59:26 +0000 [warn]: #0 /fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin_helper/thread.rb:78:in `block in thread_create'
2020-07-28 14:59:26 +0000 [warn]: #0 emit transaction failed: error_class=IOError error="closed stream" location="/fluentd/vendor/bundle/ruby/2.6.0/gems/fluentd-1.11.1/lib/fluent/plugin/buffer/file_chunk.rb:82:in `pos'" tag="kubernetes.var.log.containers.test.log"
  2020-07-28 14:59:26 +0000 [warn]: #0 suppressed same stacktrace
2020-07-28 14:59:26 +0000 [warn]: #0 [out_es] chunk bytes limit exceeds for an emitted event stream: 2493080bytes
2020-07-28 14:59:27 +0000 [warn]: #0 [out_es] chunk bytes limit exceeds for an emitted event stream: 5036846bytes
...
```


## Cleanup docker container and log

Ctrl-C on fluentd terminal.

```
docker stop es
```

```
rm -f log/*
```

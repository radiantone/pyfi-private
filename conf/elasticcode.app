
limit_req_zone $binary_remote_addr zone=one:10m rate=40r/m;
limit_conn_zone $binary_remote_addr zone=addr:10m;

proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;


server {
    listen   80;
    listen   [::]:80;

    server_name app.elasticcode.ai;

    return 301 https://app.elasticcode.ai$request_uri;
}

server {
    listen   443  ssl;

    server_name app.elasticcode.ai;

    client_body_timeout 5s;
    client_header_timeout 5s;

    client_max_body_size 50m;

    ssl    on;

    ssl_certificate    /etc/nginx/certs/elasticcode.crt;
    ssl_certificate_key    /etc/nginx/certs/elasticcode.key;

    access_log /var/log/nginx/nginx.vhost.access.log;
    error_log /var/log/nginx/nginx.vhost.error.log;

    access_log   logs/domain1.access.log  main;
    root         /var/share/html;

    underscores_in_headers on;
    proxy_read_timeout 5m;

    if ($http_origin ~* (.*\.elasticcode.ai)) {
        set $cors "true";
    }

    location /api {
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
      proxy_set_header X-NginX-Proxy true;

      proxy_pass http://api_servers/;
      proxy_redirect off;
    }

    location /socket.io/ {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $host;

      proxy_pass http://socketio_servers;

      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
    }

    location ~ ^/(images|javascript|js|css|fonts|icons||img|js|flash|media|static)/  {
      root    /var/share/html;
      expires 30d;
    }

}

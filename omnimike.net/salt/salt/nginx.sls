nginx:
  pkg:
    - installed
  service.running:
    - enable: True
    - watch:
      - pkg: nginx
      - file: /etc/nginx/nginx.conf

/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx.conf
    - user: root
    - group: root
    - mode: 644


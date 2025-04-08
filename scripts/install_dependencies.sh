version: 0.0
os: linux
files:
  - source: /    
    destination: /var/www/myapp/
    overwrite: true  

hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 180
      runas: root

  ApplicationStart:
    - location: scripts/start_application.sh
      timeout: 180
      runas: root
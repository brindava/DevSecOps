version: 0.0
os: linux
files:
  - source: /    # This refers to the root of your source directory (e.g., all files in your repo).
    destination: /var/www/myapp/
    overwrite: true  # The destination directory on the EC2 instance.

hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 180
      runas: root

  ApplicationStart:
    - location: scripts/start_application.sh
      timeout: 180
      runas: root
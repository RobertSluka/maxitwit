# -*- mode: ruby -*-
# vi: set ft=ruby :
#
Vagrant.configure("2") do |config|
  config.vm.box = 'digital_ocean'
  config.vm.box_url = "https://github.com/devopsgroup-io/vagrant-digitalocean/raw/master/box/digital_ocean.box"
  config.ssh.private_key_path = '~/.ssh/id_rsa'
  # config.vm.define "proxy", primary: true do |server|
  #   server.vm.provider :digital_ocean do |provider|
  #     provider.ssh_key_name = ENV["SSH_KEY_NAME"]
  #     provider.token = ENV["DIGITAL_OCEAN_TOKEN"]
  #     provider.image = 'ubuntu-22-04-x64'
  #     provider.region = 'fra1'
  #     provider.size = 's-1vcpu-1gb'
  #     provider.privatenetworking = true
  #   end
  #   server.vm.hostname = "proxy"
  # end
  config.vm.synced_folder '.', '/maxitwit', type: "rsync"
  config.vm.define "swarmManager", primary: true do |server|
    server.vm.provider :digital_ocean do |provider|
      provider.ssh_key_name = ENV["SSH_KEY_NAME"]
      provider.token = ENV["DIGITAL_OCEAN_TOKEN"]
      provider.image = 'ubuntu-22-04-x64'
      provider.region = 'fra1'
      provider.size = 's-1vcpu-1gb'
      provider.privatenetworking = true
    end
    # server.vm.network "forwarded_port", guest: 3000, host: 3000
    server.vm.hostname = "swarmManager"
    server.vm.provision "shell", inline: 'echo "export DOCKER_USERNAME=' + "'" + ENV["DOCKER_USERNAME"] + "'" + '" >> ~/.bash_profile'
    server.vm.provision "shell", inline: 'echo "export DOCKER_PASSWORD=' + "'" + ENV["DOCKER_PASSWORD"] + "'" + '" >> ~/.bash_profile'
    server.vm.provision "shell", inline: 'echo "export DIGITAL_OCEAN_TOKEN=' + "'" + ENV["DIGITAL_OCEAN_TOKEN"] + "'" + '" >> ~/.bash_profile'
    server.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    # The following address an issue in DO's Ubuntu images, which still contain a lock file
    sudo killall apt apt-get
    sudo rm /var/lib/dpkg/lock-frontend
    # Install docker and docker compose
    sudo apt-get install -y docker.io docker-compose-v2
    sudo systemctl status docker
    echo -e "\nOpening port for minitwit ...\n"
    ufw allow 3000 && \
    ufw allow 3001 && \
    ufw allow 22/tcp
    echo -e "\nOpening necessary ports for Docker Swarm...\n"
    ufw allow 2377/tcp
    ufw allow 7946/tcp
    ufw allow 7946/udp
    ufw allow 4789/udp
    echo -e "\nInitializing Docker Swarm...\n"
    docker swarm init --advertise-addr $(hostname -I | awk '{print $1}')
    echo ". $HOME/.bashrc" >> $HOME/.bash_profile
    echo -e "\nConfiguring credentials as environment variables...\n"
    source $HOME/.bash_profile
    echo -e "\nSelecting Minitwit Folder as default folder when you ssh into the server...\n"
    echo "cd /maxitwit" >> ~/.bash_profile
    echo "setting up swarm manager ..."
  
    chmod +x /maxitwit/remote_files/deploy.sh
    echo -e "\nVagrant setup done ..."
    echo -e "maxitwit will later be accessible at http://$(hostname -I | awk '{print $1}'):3000"
    # echo -e "\nRetrieving Swarm join token and manager IP address...\n"
    # SWARM_JOIN_TOKEN=$(docker swarm join-token -q worker)
    # MANAGER_IP=$(hostname -I | awk '{print $1}')
    # echo "SWARM_JOIN_TOKEN=$SWARM_JOIN_TOKEN" >> /vagrant/swarm.env
    # echo "MANAGER_IP=$MANAGER_IP" >> /vagrant/swarm.env
    SHELL
    # Trigger to start worker1 and worker2 after swarmmanager is fully provisioned
    config.trigger.after :provision do |trigger|
      trigger.run = { inline: "vagrant up worker1" }
      trigger.run = { inline: "vagrant up worker2" }
  end
 end
 config.vm.define "worker1", primary: true do |server|
  config.vm.synced_folder '.', '/maxitwit', type: "rsync"
  server.vm.provider :digital_ocean do |provider|
    provider.ssh_key_name = ENV["SSH_KEY_NAME"]
    provider.token = ENV["DIGITAL_OCEAN_TOKEN"]
    provider.image = 'ubuntu-22-04-x64'
    provider.region = 'fra1'
    provider.size = 's-1vcpu-1gb'
    provider.privatenetworking = true
  end
  server.vm.hostname = "worker1"
  server.vm.provision "shell", inline: <<-SHELL
  sudo apt-get update
  # The following address an issue in DO's Ubuntu images, which still contain a lock file
  sudo killall apt apt-get
  sudo rm /var/lib/dpkg/lock-frontend
  # Install docker and docker compose
  sudo apt-get install -y docker.io docker-compose-v2
  sudo systemctl status docker
  echo -e "\nJoining Docker Swarm...\n"
  SWARM_JOIN_TOKEN=$(vagrant ssh swarmManager -c "docker swarm join-token -q worker")
  MANAGER_IP=$(vagrant ssh swarmManager -c "hostname -I | awk '{print $1}'")
  docker swarm join --token $SWARM_JOIN_TOKEN $MANAGER_IP:2377
  SHELL
 end
 config.vm.define "worker2", primary: true do |server|
  config.vm.synced_folder '.', '/maxitwit', type: "rsync"
  server.vm.provider :digital_ocean do |provider|
    provider.ssh_key_name = ENV["SSH_KEY_NAME"]
    provider.token = ENV["DIGITAL_OCEAN_TOKEN"]
    provider.image = 'ubuntu-22-04-x64'
    provider.region = 'fra1'
    provider.size = 's-1vcpu-1gb'
    provider.privatenetworking = true
  end
  server.vm.hostname = "worker2"
  server.vm.provision "shell", inline: <<-SHELL
  sudo apt-get update
  # The following address an issue in DO's Ubuntu images, which still contain a lock file
  sudo killall apt apt-get
  sudo rm /var/lib/dpkg/lock-frontend
  # Install docker and docker compose
  sudo apt-get install -y docker.io docker-compose-v2
  sudo systemctl status docker
  echo -e "\nJoining Docker Swarm...\n"
  SWARM_JOIN_TOKEN=$(vagrant ssh swarmManager -c "docker swarm join-token -q worker")
  MANAGER_IP=$(vagrant ssh swarmManager -c "hostname -I | awk '{print $1}'")
  docker swarm join --token $SWARM_JOIN_TOKEN $MANAGER_IP:2377
  SHELL
 end
  # config.vm.define "monitoring", primary: true do |server|
  #   server.vm.provider :digital_ocean do |provider|
  #     provider.ssh_key_name = ENV["SSH_KEY_NAME"]
  #     provider.token = ENV["DIGITAL_OCEAN_TOKEN"]
  #     provider.image = 'ubuntu-22-04-x64'
  #     provider.region = 'fra1'
  #     provider.size = 's-1vcpu-1gb'
  #     provider.privatenetworking = true
  #   end
  #   server.vm.hostname = "monitoring"
  # end
 end
 export DIGITALOCEAN_PRIVATE_NETWORKING=true
 export DROPLETS_API="https://api.digitalocean.com/v2/droplets"
 export BEARER_AUTH_TOKEN="Authorization: Bearer $DIGITAL_OCEAN_TOKEN"
 export JSON_CONTENT="Content-Type: application/json"
 CONFIG='{"name":"swarm-manager","tags":["demo"],
  "size":"s-1vcpu-1gb", "image":"docker-20-04",
  "ssh_keys":["69:d8:8a:dc:08:c7:0d:a5:5d:7d:3d:de:91:ae:f0:c7"]}'
 SWARM_MANAGER_ID=$(curl -X POST "$DROPLETS_API" -d "$CONFIG"\
  -H "$BEARER_AUTH_TOKEN" -H "$JSON_CONTENT"\
  | jq -r .droplet.id ) && sleep 5 && echo $SWARM_MANAGER_ID
 export JQFILTER='.droplets | .[] | select (.name == "swarm-manager")
 | .networks.v4 | .[]| select (.type == "public") | .ip_address'
 SWARM_MANAGER_IP=$(curl -s GET "$DROPLETS_API"\
  -H "$BEARER_AUTH_TOKEN" -H "$JSON_CONTENT"\
  | jq -r "$JQFILTER") && echo "SWARM_MANAGER_IP=$SWARM_MANAGER_IP"
 
 
  # Commenting
  WORKER1_ID=$(curl -X POST "$DROPLETS_API"\
       -d'{"name":"worker1","tags":["demo"],"region":"fra1",
       "size":"s-1vcpu-1gb","image":"docker-20-04",
       "ssh_keys":["69:d8:8a:dc:08:c7:0d:a5:5d:7d:3d:de:91:ae:f0:c7"]}'\
       -H "$BEARER_AUTH_TOKEN" -H "$JSON_CONTENT"\
       | jq -r .droplet.id )\
       && sleep 3 && echo $WORKER1_ID
 
 
 
 
 export JQFILTER='.droplets | .[] | select (.name == "worker1") | .networks.v4 | .[]| select (.type == "public") | .ip_address'
 
 
 
 
 WORKER1_IP=$(curl -s GET "$DROPLETS_API"\
    -H "$BEARER_AUTH_TOKEN" -H "$JSON_CONTENT"\
    | jq -r "$JQFILTER")\
    && echo "WORKER1_IP=$WORKER1_IP"
 
 
      # Commenting
  WORKER2_ID=$(curl -X POST "$DROPLETS_API"\
  -d'{"name":"worker2","tags":["demo"],"region":"fra1",
  "size":"s-1vcpu-1gb","image":"docker-20-04",
  "ssh_keys":["69:d8:8a:dc:08:c7:0d:a5:5d:7d:3d:de:91:ae:f0:c7"]}'\
  -H "$BEARER_AUTH_TOKEN" -H "$JSON_CONTENT"\
  | jq -r .droplet.id )\
  && sleep 3 && echo $WORKER2_ID
 
 
 
 
 export JQFILTER='.droplets | .[] | select (.name == "worker2") | .networks.v4 | .[]| select (.type == "public") | .ip_address'
 
 
 
 
 WORKER2_IP=$(curl -s GET "$DROPLETS_API"\
 -H "$BEARER_AUTH_TOKEN" -H "$JSON_CONTENT"\
 | jq -r "$JQFILTER")\
 && echo "WORKER2_IP=$WORKER2_IP"
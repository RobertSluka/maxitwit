# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Specify the base image for the virtual machine
  config.vm.box = 'digital_ocean'
  config.vm.box_url = "https://github.com/devopsgroup-io/vagrant-digitalocean/raw/master/box/digital_ocean.box"

  # Specify the path to the private SSH key to be used when connecting to the VM
  config.ssh.private_key_path = '~/.ssh/id_rsa'

  # Set up a synced folder between your host machine and the VM
  config.vm.synced_folder ".", "/vagrant", type: "rsync"

  # Define a VM named "webserver"
  config.vm.define "webserver", primary: false do |server|

    # Configure the VM to be created on DigitalOcean
    server.vm.provider :digital_ocean do |provider|
      provider.ssh_key_name = ENV["SSH_KEY_NAME"]
      provider.token = ENV["DIGITAL_OCEAN_TOKEN"]
      provider.image = 'ubuntu-22-04-x64'
      provider.region = 'fra1'
      provider.size = 's-1vcpu-1gb'
      provider.privatenetworking = true
    end

    # Set the hostname of the VM to "webserver"
    server.vm.hostname = "webserver"      

  end

  # Run a shell script on the VM after it's created
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
  SHELL

  # Install Docker and Docker Compose on the VM
  config.vm.provision :docker
  config.vm.provision :docker_compose, yml: "/vagrant/compose.yml", run: "always"
end
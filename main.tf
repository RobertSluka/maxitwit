provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "web" {
  image  = "ubuntu-20-04-x64"
  name   = "testing"
  region = "nyc2"
  size   = "s-1vcpu-1gb"
}
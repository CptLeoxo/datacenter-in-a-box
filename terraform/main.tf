terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }

}

resource "docker_image" "flask_app_image" {
  name = "datacenter-flask:latest"

  build {
    context = "../app"
  }
}

resource "docker_network" "datacenter_net" {
  name = "datacenter_net"
}

resource "docker_container" "flask_app" {
  name = "flask_app"

  image = docker_image.flask_app_image.name

  networks_advanced {
    name = docker_network.datacenter_net.name
  }

  ports {
    internal = 5000
    external = 5000
  }
}

resource "docker_image" "nginx_image" {
  name = "nginx:alpine"
}

resource "docker_container" "nginx" {
  name  = "nginx_proxy"
  image = docker_image.nginx_image.name

  networks_advanced {
    name = docker_network.datacenter_net.name
  }

  ports {
    internal = 80
    external = 80
  }

  volumes {
    host_path      = abspath("../nginx/nginx.conf")
    container_path = "/etc/nginx/nginx.conf"
    read_only      = true

  }
}

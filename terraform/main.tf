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

  env = [
    "DB_HOST=postgres_db",
    "DB_USER=${var.db_user}",
    "DB_PASSWORD=${var.db_password}",
    "DB_NAME=datacenter"

  ]

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

resource "docker_volume" "postgres_data" {
  name = "pg_data"
}

resource "docker_image" "postgres_image" {
  name = "postgres:15-alpine"
}

resource "docker_container" "postgres" {
  name  = "postgres_db"
  image = docker_image.postgres_image.name

  networks_advanced {
    name = docker_network.datacenter_net.name
  }

  env = [
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=datacenter"
  ]

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

}


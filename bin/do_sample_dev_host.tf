variable "do_token" {}
variable "pub_key" {}
variable "pvt_key" {}
variable "ssh_fingerprint" {}
variable "droplet_name" {}

provider "digitalocean" {
    token = "${var.do_token}"
}

resource "digitalocean_droplet" "web" {
    image = "ubuntu-18-04-x64"
    name = "${var.droplet_name}"
    region = "ams3"
    size = "s-2vcpu-2gb"
    private_networking = true
    ssh_keys = [
      "${var.ssh_fingerprint}"
    ]

    connection {
        user = "root"
        type = "ssh"
        private_key = "${file(var.pvt_key)}"
        timeout = "2m"
    }

    provisioner "remote-exec" {
        inline = [
            "apt-get update",
            "apt install -y docker.io",
            "systemctl enable docker",
            "docker run --name redis -p 7001:6379 -d redis",
            "docker pull rabbitmq",
            "docker run -d --hostname my-rabbit --name some-rabbit -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 15672:15672 rabbitmq",
            "docker exec some-rabbit rabbitmq-plugins enable rabbitmq_management"
        ]
    }
}
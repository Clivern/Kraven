Run Sample Host on DigitalOcean
===============================

$ terraform init

# Get SSH Fingerprint
$ ssh-keygen -lf ~/.ssh/id_rsa.pub

$ terraform plan \
    -var "do_token=$YOUR_TOKEN" \
    -var "pub_key=~/.ssh/id_rsa.pub" \
    -var "pvt_key=~/.ssh/id_rsa" \
    -var "ssh_fingerprint=$SSH_FINGERPRINT" \
    -var "droplet_name=$DROPLET_NAME"


$ terraform apply \
    -var "do_token=$YOUR_TOKEN" \
    -var "pub_key=~/.ssh/id_rsa.pub" \
    -var "pvt_key=~/.ssh/id_rsa" \
    -var "ssh_fingerprint=$SSH_FINGERPRINT" \
    -var "droplet_name=$DROPLET_NAME"

$ terraform show terraform.tfstate
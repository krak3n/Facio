#!/usr/bin/ruby

#
# Vagrant File for Facio
# Provisioner: Salt
# OS: Ubuntu 12.04 LTS 64Bit
#

Vagrant::Config.run do |config|

    # Base Box - http://www.vagrantbox.es/
    config.vm.box = "ubuntu_precise64_vagrant"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    #
    # Shares
    #

    # The Project Mount - This Directory
    config.vm.share_folder("v-root", "/home/vagrant/facio", ".", :nfs => true)

    # Project Salt Sates
    config.vm.share_folder("salt_file_root", "/srv/salt", "./salt")

    # Local Developer States - Not in version control, this is for the developer to manage, e.g Git / Vim Configs
    # Developers should symlink this locally to ~/.salt-dev
    if File.directory?(File.join(File.expand_path('~'), '.salt-dev'))
        config.vm.share_folder("salt-local", "/home/vagrant/.salt-dev", File.join(File.expand_path('~'), '.salt-dev'))
    else
        $stdout.write "Info: You do not have any local states\n"
    end

    #
    # Port Forwarding
    #

    config.vm.forward_port 80, 8080
    config.vm.network :hostonly, "10.10.10.10"

    #
    # Enable Symlink Support
    #
    config.vm.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]

    #
    # Provisioner: Salt: http://saltstack.com/
    #

    config.vm.provision :salt do |salt|
        salt.run_highstate = true                           # Always run the Salt Proviosining System
        salt.minion_config = "salt/config/minion.conf"      # Where the minion config lives
        salt.salt_install_type = "stable"
    end

end

#!/usr/bin/ruby

#
# Vagrant File for Facio - Requires Vagrant 1.1+
# Provisioner: Salt
# OS: Ubuntu 12.04 LTS 64Bit
#

Vagrant.configure("2") do |config|

    # Base Box - http://www.vagrantbox.es/
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    #
    # Port Forwarding / Assign static IP
    #

    config.vm.network :private_network, ip: "10.10.10.10"

    #
    # Virutalbox Settings
    #
    config.vm.provider :virtualbox do |v|
        v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    #
    # Synced Folders
    #

    # The Project Mount - This Directory
    config.vm.synced_folder ".", "/home/vagrant/facio", :nfs => true

    # Salt States
    config.vm.synced_folder "./salt", "/srv/salt"

    # Local Developer States - Not in version control, this is for the developer to manage, e.g Git / Vim Configs
    # Developers should symlink this locally to ~/.salt-dev
    local_developer_states = File.join(File.expand_path('~'), '.salt')
    if File.directory?(local_developer_states)
        config.vm.synced_folder local_developer_states, "/home/vagrant/.salt"
    else
        $stdout.write "Vagrant: Warning: You do not have any local states\n"
    end

    #
    # Provisioner: Salt
    #

    config.vm.provision :salt do |s|
        s.run_highstate = true                           # Always run the Salt provisioning system
        s.minion_config = "salt/config/minion.conf"      # Where the minion config lives
        s.install_type = "stable"
    end

end

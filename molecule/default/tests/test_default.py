"""Molecule tests for the default scenario."""

import os

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_nix_config(host):
    """Test that nix was installed as expected."""
    config_dir = host.file("/home/molecule/.config")
    nix_conf = host.file("/home/molecule/.config/nix/nix.conf")

    assert config_dir.is_directory
    assert config_dir.mode == 0o0755
    assert config_dir.user == "molecule"
    assert nix_conf.is_file
    assert nix_conf.mode == 0o0644
    assert nix_conf.user == "molecule"
    assert "nix-command flakes" in nix_conf.content_string


def test_nix_installed(host):
    """Test that nix was installed as expected."""
    nix_dir = host.file("/nix")
    nix_channels = host.file("/home/molecule/.nix-channels")

    assert nix_dir.is_directory
    assert nix_dir.mode == 0o0755
    assert nix_dir.user == "molecule"
    assert nix_dir.group == "root"
    assert nix_channels.is_file
    assert nix_channels.mode == 0o0644
    assert nix_channels.user == "molecule"
    assert nix_channels.group == "molecule"


def test_nix_package_installed(host):
    """Test that the example nix package was installed successfully."""
    hello_package_link = host.file("/home/molecule/.nix-profile/bin/hello")
    hello_package_file = host.file(hello_package_link.linked_to)

    assert hello_package_link.is_symlink
    assert hello_package_link.user == "molecule"
    assert hello_package_link.group == "molecule"
    assert hello_package_file.is_file
    assert hello_package_file.mode == 0o0555
    assert hello_package_file.user == "molecule"
    assert hello_package_file.group == "molecule"

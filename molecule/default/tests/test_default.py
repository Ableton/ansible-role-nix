"""Molecule tests for the default scenario."""

import os

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


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

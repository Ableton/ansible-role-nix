Ansible role ableton.nix
========================

This role installs the [Nix][nix] software on the given Ansible host and configures it for
a given user. It also optionally sets up [Nix Flakes][nix flakes].

Note that any logged-in users who want to use Nix must restart their shells after this
role has been applied.

Requirements
------------

Ansible >= 2.10, and a target host running either a Debian-flavor of Linux or macOS. Other
Linux flavors will probably work with this role, but they haven't been tested.

Role Variables
--------------

See the [`defaults/main.yml`](defaults/main.yml) file for full documentation on required
and optional role variables.

Example Playbook
----------------

```yaml
---
- name: Install Nix on hosts
  hosts: "all"

  roles:
    - ableton.nix
```

License
-------

MIT

Maintainers
-----------

This project is maintained by the following GitHub users:

- [@ala-ableton](https://github.com/ala-ableton)
- [@nre-ableton](https://github.com/nre-ableton)


[nix]: https://nixos.org/nix
[nix flakes]: https://nixos.wiki/wiki/Flakes

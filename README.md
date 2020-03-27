# The Foreman Release Tool

## Design

The Foreman Release Tool should support the release team in their tasks to craft a full release.

This includes:
* GPG key maintenance
* branching and tagging the Git repositories
* generating tarballs and Ruby gems
* signing tarballs
* uploading tarballs and Ruby gems
* preparing packaging changes
* signing packages

## Configuration

The `releasetool.yaml` file contains the project definitions and their configuration. It can be read as an Ansible Inventory.

At the top level, there are the various projects we support (Foreman, Katello, Pulp) and default variables that apply to all projects.

Each project can later define their own, project-specific, settings. The last level is the versioned project definition, which usually will just inherit from the main project definition and define version-specific data (the version itself and the signing key).

## Dependencies

* Ansible
* Obsah
* Koji
* GnuPG2
* gopass

## Usage

The general usage of the tool is to call `releasetool ACTION PROJECT-VERSION`. Executing actions against the unversioned project definitions is not supported.

If at any step the system asks you for the password to a GPG key, use crtl+v to paste the secret that was copied automatically to the clipboard.

### Import GPG Key

Before running most actions the associated GPG key will need to be imported. Example:

```
releasetool import-gpg-private foreman-2.0
```

### Generating release tarballs and Ruby gems

This action will take the source code from Git and generate release tarballs and Ruby gems that can be uploaded.

To generate the Foreman 1.23.0 tarballs, execute `releasetool build-source foreman-1.23`

To generate the Katello 3.13.0 gem, execute `releasetool build-source katello-3.13`

### Signing RPMs

This action will contact Koji, list all RPMs for that release, find the ones that are not signed with the current release key, download these, `rpmsign` them and upload the signatures back to Koji.

To sign the Katello 3.13.0 release, execute `releasetool sign-rpms katello-3.13`.

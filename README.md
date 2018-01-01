# PowerGrid 
# CMPT 318-D2 Group 6 Cyber Security Final Project

This repository contains all work associated with the final course project.

The goal is to develop an anomaly detection system for use with a power grid data set.

## Repository Guidelines

Since this repository is a shared space, lets keep it clean. Here are a few guidelines which will help acheive this:

1. Always branch
    - Perform work on your own personal branch
    - Create a merge request for 'develop' when your work is ready
        Note: _The branch can be anything except for 'master', which is protected from direct commits_
    - Assign a team member to peer review your merge request
2. Use issues for:
    - Suggestions
    - Discussion
    - Help
    - Bugs
3. Thats it!

## Getting started

We will be using [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/). The repository contains a _Vagrantfile_ which handles environment setup. All you need to do is:

1. Install the latest stable versions 
    - [Vagrant 1.9.7](https://www.vagrantup.com/downloads.html)
    - [VirtualBox 5.1.22](https://www.virtualbox.org/wiki/Downloads)
2. `vagrant up` from the repository directory
3. `vagrant ssh` to log in to the box. We are using Ubuntu 16.04
5. `exit` followed by `vagrant halt` to shutdown the virtual machine
4. Any changes to the environment will be provided through the _Vagrantfile_. When you pull changes, you can reload the box to get these updates. If you have problems with the setup, or would like to suggest a required environment change (dependancy) please raise an issue!

## File Structure

The Vagrant box can access the entire repository directory. There are 4 main subdirectories:

1. source
    - All source files
2. results
    - Any reports generated
3. data
    - All the test and trainning data lives here
4. scripts
   - Setup or runner files
   
## Code Style

Follow the [python style guide](https://www.python.org/dev/peps/pep-0008/) as much as possible. Some basic guidelines are:

1. Spaces not tabs
    - 4 spaces indentation
    - line continuations are indented 8 spaces
2. Names
    - Classes are CamelCase
    - Variables and functions are lower\_separated
    - Private members are \_prefixed\_lower\_separated
    - Files are lower\_separated
    - Keyword conflicts are resolved by appending the keyword with an underscore



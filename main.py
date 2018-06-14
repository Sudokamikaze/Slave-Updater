#!/bin/python

import docker
import subprocess
import git 
import os
import configparser

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

class MAINC:
    __parser = configparser.ConfigParser()
    __repo_url = "https://github.com/Sudokamikaze/Slave.git"
    __repo_dir = "/tmp/Slave"
    __config_file = "env.config"
    __Jsecret = ""
    __Jn_Name = ""
    __Jm_IP = ""
    __Jm_Port = ""

    def __init__(self):
        try:
            client.ping()
        except docker.errors.APIError:
            print('No connection to Docker Engine, exiting...')
            os.sys.exit(1)

        self.__parser.read(self.__config_file)
        self.check_for_updates()

    def check_for_updates(self):
        if os.path.isdir(self.__repo_dir) == False:
            print('Clonning repo')
            git.Repo.clone_from("https://github.com/Sudokamikaze/Slave.git", self.__repo_dir)
            print('Starting container update procedure')
            self.calling_docker()

        else:
            if self.puller() == "Nothing to do":
                print('There is nothing to do, exiting...')
                os.sys.exit(0)
            else:
                print('Starting container update procedure')
                self.calling_docker()

    def puller(self):
        if git.cmd.Git(self.__repo_dir).pull() == "Already up to date.":
            valuetoreturn = "Nothing to do"
        else:
            valuetoreturn = "Repo is updated"
        
        return valuetoreturn
         
    def calling_docker(self):
        container = client.containers.get('Jenkins_slave')
        container.stop()
        container.remove()
        client.images.remove('slave')
        try:
            client.images.build(path='/tmp/Slave', nocache=True, tag='slave:latest',
            buildargs={
            'Jenkins_Secret': self.__parser['DEFAULT']['Jenkins_Secret'],
            'Jenkins_Node_Name': self.__parser['DEFAULT']['Jenkins_Node_Name'],
            'Jenkins_Master_IP': self.__parser['DEFAULT']['Jenkins_Master_IP'],
            'Jenkins_Master_Port': self.__parser['DEFAULT']['Jenkins_Master_Port']
                      }
            ) 
        except docker.errors.BuildError:
            print('There is something went wrong')
            os.sys.exit(1)
        
        client.containers.run(image='slave', detach=True, name='Jenkins_slave', network_mode='bridge', 
        volumes={
        'slave_data': {'volume':'/home/jenkins', 'mode': 'rw'}
        })
        
        print('Finished updaing Docker container! Git HEAD was {}'.format(git.Repo(self.__repo_dir).repo.head.commit))

classcall = MAINC()

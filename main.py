#!/bin/python

import docker
import subprocess
from git 
import os
import configparser

client = docker.from.env()
parser = configparser.ConfigParser()

class MAINC:
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

        self.__Jsecret = parser['SD']['Jenkins_Secret']
        self.__Jn_Name = parser['SD']['Jenkins_Node_Name']
        self.__Jm_IP   = parser['SD']['Jenkins_Master_IP']
        self.__Jm_Port = parser['SD']['Jenkins_Master_Port']
        self.check_for_updates()

    def check_for_updates(self):
        if os.path.isdir(self.__repo_dir) == False:
            git.Repo.clone_from("https://github.com/Sudokamikaze/Slave.git", self.__repo_dir)
        else:
            if self.puller() == "Nothing to do":
                os.sys.exit(0)
            else:
                self.calling_docker()

    def puller(self):
        if git.cmd.Git(self.__repo_dir).pull() == "Already up to date.":
            valuetoreturn = "Nothing to do"
        else:
            valuetoreturn = "Repo is updated"
        
        return valuetoreturn
         
    def calling_docker(self):
        client.containers.stop('Jenkins_slave')
        client.containers.remove('Jenkins_slave')
        client.images.remove('Slave')
        try:
            client.build(path='/tmp/Slave', nocache=True, tag='Slave:latest',
            buildargs={
            'Jenkins_Secret': self.__Jsecret,
            'Jenkins_Node_Name': self.__Jn_Name,
            'Jenkins_Master_IP': self.__Jm_IP,
            'Jenkins_Master_Port': self.__Jm_Port
                      }
            ) 
        except docker.errors.BuildError:
            print('There is something went wrong')
            os.sys.exit(1)
        
        client.containers.run(image='Slave', detach=True, name='Jenkins_slave', network_mode='bridge', volumes={'slave_data': {'volume':'/home/jenkins', 'mode', 'rw'}})
        print('Finished updaing Docker container! Git HEAD was {}'.format(git.Repo(self.__repo_dir).repo.head.commit))

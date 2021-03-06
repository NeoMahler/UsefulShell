#!/usr/bin/env python3
import logging, logging.handlers
import logging.config
from ftplib import *


class FTPConnect:

    """ Connects to an ftp server """
    def __init__(self, host, port, user, passwd):
        """  Connection to ftp __init__ """
        ftplog = logging.getLogger('ftpserver')
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        with FTP(self.host, self.user, self.passwd) as ftp:
            ftp.login(self.user, self.passwd)
            ftp.getwelcome()
            ftp.retrlines('LIST')
            try:
                while True:
                    inp = input(self.user + '@' + self.host + " " + ftp.pwd() + '> ')
                    shell = inp.split()
                    ftplog.info(inp)
                    try:
                        print(ftp.sendcmd(inp))
                    except:
                        try:
                            if "retrbinary" in shell:
                                print(ftp.retrbinary(shell[1]))
                            elif "retrlines" in shell:
                                print(ftp.retrlines(shell[1]))
                            elif "set_pasv" in shell:
                                print(ftp.set_pasv(shell[1]))
                            elif "storbinary" in shell:
                                print(ftp.storbinary(shell[1], shell[2]))
                            elif "storlines" in shell:
                                print(ftp.storlines(shell[1], shell[2]))
                            elif "transfercmd" in shell:
                                print(ftp.transfercmd(shell[1]))
                            elif "ntransfercmd" in shell:
                                print(ftp.ntrasfercmd(shell[1]))
                            elif "mlsd" in shell:
                                print(ftp.mlsd(path=shell[1], facts=[]))
                            elif "nlst" in shell:
                                list = ftp.nlst()
                                strnlst = "\n".join(list)
                                print(strnlst)
                            elif "rename" in shell:
                                print(ftp.rename(shell[1], shell[2]))
                            elif "delete" in shell:
                                print(ftp.delete(shell[1]))
                            elif "cwd" or "cd" in shell:
                                print(ftp.cwd(shell[1]))
                            elif "mkd" or "mkdir" in shell:
                                print(ftp.mkd(shell[1]))
                            elif "pwd" in shell:
                                print(ftp.pwd())
                            elif "rmd" or "rmdir" in shell:
                                 print(ftp.rmd(shell[1]))
                            elif "size" in shell:
                                print(ftp.size(shell[1]))
                            elif inp == "":
                                continue
                            #elif "upload" in shell: Trying to upload...
                                #try:
                                    #file = open(shell[1], 'rb')
                                    #print(ftp.storbinary('STOR ' + shell[1], file))
                                    #file.close()
                                #except IndexError:
                                    #print("Syntax: upload <path_to_file>")

                            else:
                                print('500 Unknown command')

                        except IndexError:
                            if shell[0] == "upload":
                                print("Syntax: upload <path_to_file>")
                            else:
                                print('500 Unknown command')
                        except:
                            print("550 Error")
            except EOFError:
                pass
            except KeyboardInterrupt:
                pass


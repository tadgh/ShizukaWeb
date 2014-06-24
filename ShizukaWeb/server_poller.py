import logging
import Pyro4
import time
from celery import Task


class ServerPoller(Task):

    def __init__(self):
        abstract = True
        self._ns = None
        self._reporting_server = None

    @property
    def reporting_server(self):
        logging.info("Calling RS!")
        try:
            if self._reporting_server is None or not self._reporting_server.ping():
                logging.info("NS IS NONE")
                self.reconnect_to_server()
                return self._reporting_server
            else:
                logging.info("NS EXISTS PASSING IT")
                return self._reporting_server
        except Exception as e:
            logging.error("Trouble in getting the reporting server: " + str(e))
            self.reconnect_to_server()
            return self._reporting_server

    def set_server(self, reporting_server, server_name):
        if self._reporting_server is None:
            logging.info("Initializing server for the first time --> Found Server : {} ".format(server_name))
        else:
            logging.warning("Server being re-assigned. : {} ".format(server_name))
        self._reporting_server = reporting_server

    ## Called when unable to execute methods on remote server. Continuously attempts re-connection to Server and attempts
    # ping. When it succeeds, it sets the server and returns control to where it was called.
    def reconnect_to_server(self):
        disconnected = True
        while disconnected:
            try:
                name_server = Pyro4.locateNS()
                server_dict = name_server.list(prefix="shizuka.server.")
                server_name, server_uri = server_dict.popitem()

                if server_uri:
                    logging.info("Found Server named: {} . Joining...".format(server_name))
                    reporting_server = Pyro4.Proxy(server_uri)
                    self.set_server(reporting_server, server_name)
                try:
                    self._reporting_server.ping()
                    logging.info("Ping succeeded on server. Returning control to polling thread.")
                    disconnected = False
                except AttributeError as e:
                    logging.error("Unable to ping server: Error message: {}".format(str(e)))
            except KeyError as e:
                logging.error("Found Nameserver, but couldn't find Server Object. Error Message: {}".format(str(e)))
            except Pyro4.errors.NamingError as e:
                logging.error("Unable to find NameServer for Pyro4. Is it running? Error message: {}".format(str(e)))
            except Exception as e:
                logging.error("Unknown error occurred attempting to reconnect to server. Error Message : {}".format(e))
            time.sleep(5)


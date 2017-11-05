"""Module to listen for homee events."""
import collections
import json
import logging
import time
import threading
import websocket
from pyhomee.util import get_token
from pyhomee.attribute import Attribute

_LOGGER = logging.getLogger(__name__)


class SubscriptionRegistry(object):
    """Class for subscribing to homee events."""

    def __init__(self, cube):
        """Setup websocket."""
        self.cube = cube
        self.hostname = cube.hostname
        self._nodes = collections.defaultdict(list)
        self._callbacks = collections.defaultdict(list)
        self._exiting = False
        self._event_loop_thread = None

    def register(self, node, callback):
        """Register a callback.

        node: node to be updated by subscription
        callback: callback for notification of changes
        """
        if not node:
            _LOGGER.error("Received an invalid node: %r", node)
            return

        _LOGGER.debug("Subscribing to events for %s", node)
        self._nodes[node.id].append(node)
        self._callbacks[node.id].append((callback))

    def join(self):
        """Don't allow the main thread to terminate until we have."""
        self._event_loop_thread.join()

    def start(self):
        """Start a thread to connect to homee websocket."""
        self._event_loop_thread = threading.Thread(target=self._run_event_loop,
                                             name='Homee Event Loop Thread')
        self._event_loop_thread.deamon = True
        self._event_loop_thread.start()

    def stop(self):
        """Tell the event loop thread to terminate."""
        self.ws.close()
        self.join()
        _LOGGER.info("Terminated thread")

    def def send_node_command(self, node, attribute, target_value)
        self.ws.send("PUT:nodes/{}/attributes/{}?target_value={}".format(node.id, attribute.id, target_value)

    def _run_event_loop(self):
        token = self.cube.get_token()
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://{}:7681/connection?access_token={}".format(self.hostname, token),
                                  subprotocols = ["v2"],
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_message(self, ws, message):
        try:
            parsed = json.loads(message)
        except:
            return
        if "attribute" in parsed:
            attribute = Attribute(parsed["attribute"])
            if attribute.node_id in self._callbacks:
                for callback in self._callbacks[attribute.node_id]:
                    callback(attribute)
        else:
            pass

    def on_error(self, ws, error):
        pass

    def on_close(self, ws):
        pass

    def on_open(self, ws):
        ws.send('ping')

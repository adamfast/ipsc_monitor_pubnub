import json

from Pubnub import Pubnub
from twisted.internet import reactor

from ipsc import IPSC, UnauthIPSC, NETWORK  # grab the config being used by the IPSC client


class PubNubIPSC(IPSC):

    def _notify_event(self, network, event, info):
        """Pass on to PubNub when an event happens that may be useful to notify the outside world about."""

        if 'PUBNUB' in NETWORK[network]:  # only proceed if configuration is present
            info['type'] = event  # set the event on the event info

            if NETWORK[network]['PUBNUB'].get(event, False) is not False:
                self.pubnub.publish({'channel': NETWORK[network]['PUBNUB'][event], 'message': json.dumps(info)})


class PubNubUnauthIPSC(UnauthIPSC):

    def _notify_event(self, network, event, info):
        """Pass on to PubNub when an event happens that may be useful to notify the outside world about."""

        if 'PUBNUB' in NETWORK[network]:  # only proceed if configuration is present
            info['type'] = event  # set the event on the event info

            if NETWORK[network]['PUBNUB'].get(event, False) is not False:
                self.pubnub.publish({'channel': NETWORK[network]['PUBNUB'][event], 'message': json.dumps(info)})


if __name__ == '__main__':
    networks = {}
    for ipsc_network in NETWORK:
        if (NETWORK[ipsc_network]['LOCAL']['ENABLED']):
            if NETWORK[ipsc_network]['LOCAL']['AUTH_ENABLED'] == True:
                networks[ipsc_network] = PubNubIPSC(ipsc_network)
            else:
                networks[ipsc_network] = PubNubUnauthIPSC(ipsc_network)

            if 'PUBNUB' in NETWORK[ipsc_network]:  # there's a pubnub config variable present for it, so instantiate the necessary class and attach it
                networks[ipsc_network].pubnub = Pubnub(NETWORK[ipsc_network]['PUBNUB']['PUBLIC_KEY'], NETWORK['IPSC1']['PUBNUB']['PRIVATE_KEY'], None, False)

            reactor.listenUDP(NETWORK[ipsc_network]['LOCAL']['PORT'], networks[ipsc_network])

    reactor.run()

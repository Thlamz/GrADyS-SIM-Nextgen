import random
from protocols.IProtocol import IProtocol
from provider.IProvider import IProvider
from messages.CommunicationCommand import SendMessageCommand
from messages.MobilityCommand import SetModeCommand, MobilityMode, ReverseCommand
from messages.Telemetry import Telemetry
from protocols.simple.SimpleMessage import SimpleMessage, SenderType


class SimpleProtocolMobile(IProtocol):
    packets: int

    def initialize(self, stage: int):
        self.packets = 0
        self.provider.send_mobility_command(SetModeCommand(MobilityMode.AUTO))

        # Scheduling self message with a random delay to prevent collision when sending pings
        self.provider.schedule_timer({}, self.provider.current_time() + random.random())

    def handle_timer(self, timer: dict):
        ping: SimpleMessage = {
            'sender': SenderType.DRONE,
            'content': self.packets
        }
        self.provider.send_communication_command(SendMessageCommand(ping))
        self.provider.schedule_timer({}, self.provider.current_time() + 1)

    def handle_message(self, message: SimpleMessage):
        if message['sender'] == SenderType.GROUND_STATION:
            self.packets = 0
            self.provider.send_mobility_command(ReverseCommand())

        elif message['sender'] == SenderType.SENSOR:
            self.packets += message['content']

    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finalize(self):
        pass

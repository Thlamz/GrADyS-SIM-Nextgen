from counter_protocol import CounterProtocol
from simulator.node.handler.communication import CommunicationHandler, CommunicationMedium
from simulator.node.handler.mobility import MobilityHandler
from simulator.node.handler.timer import TimerHandler
from simulator.node.handler.visualization import VisualizationHandler
from simulator.simulation import SimulationBuilder, SimulationConfiguration

# To enhance our viewing experience we are setting the simulation
# to real-time mode. This means that the simulation will run
# approximately synchronized with real-time, enabling us to see
# the nodes moving properly. We are also decreasing the total
# simulation time, so we don't have to wait for that long
config = SimulationConfiguration(
    duration=30,
    real_time=True
)
builder = SimulationBuilder(config)

for _ in range(10):
    builder.add_node(CounterProtocol, (0, 0, 0))

builder.add_handler(TimerHandler())

medium = CommunicationMedium(
    transmission_range=30
)
builder.add_handler(CommunicationHandler())

builder.add_handler(MobilityHandler())

# Adding visualization handler to the simulation
builder.add_handler(VisualizationHandler())

simulation = builder.build()
simulation.start_simulation()

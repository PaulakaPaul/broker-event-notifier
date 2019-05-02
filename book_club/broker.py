from common.program import Program
from common.request_reply.web_handlers import Broker

broker = Broker()

program = Program(broker, [])
program.start()

from common.program import Program
from common.request_reply.web_handlers import EventWebHandler
from network_management import events

web_handler = EventWebHandler('router')
web_handler.persist_address()

program = Program(web_handler, events.events)
program.start()


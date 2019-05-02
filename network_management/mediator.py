from common.program import Program
from common.request_reply.web_handlers import EventWebHandler

web_handler = EventWebHandler('mediator')
web_handler.persist_address()

program = Program(web_handler, [])
program.start()

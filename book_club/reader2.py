from common.program import Program
from common.request_reply.web_handlers import EventWebHandler
from book_club import events

web_handler = EventWebHandler('reader2')
web_handler.persist_address()

program = Program(web_handler, events.events)
program.start()

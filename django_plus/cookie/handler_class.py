
class HandlerClass(dict):

    def attach_to_response(self, response):
        for cookie_item in self.values():
            cookie_item.attach_to(response)
